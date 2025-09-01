import os
import markdown
from typing import List, Dict, Any
from pathlib import Path
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from sqlalchemy import create_engine, text
from ..config import settings

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def embed_docs(self, docs_path: str, collection_name: str) -> bool:
        """
        Process markdown files and store embeddings in pgvector
        
        Args:
            docs_path: Path to documentation directory
            collection_name: Name for the vector collection
            
        Returns:
            bool: Success status
        """
        try:
            # Create vector store connection
            connection_string = f"postgresql+psycopg2://{settings.DATABASE_URL.split('://')[1]}"
            vectorstore = PGVector(
                collection_name=collection_name,
                connection_string=connection_string,
                embedding_function=self.embeddings
            )
            
            # Process markdown files
            docs_path = Path(docs_path)
            documents = []
            
            for md_file in docs_path.glob("*.md"):
                if md_file.name == "README_RAG.md":
                    continue  # Skip the README file
                    
                print(f"Processing {md_file.name}...")
                
                # Read and parse markdown
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Convert markdown to plain text
                html = markdown.markdown(content)
                # Simple HTML to text conversion (you might want to use BeautifulSoup for better parsing)
                text_content = html.replace('<h1>', '# ').replace('</h1>', '\n')
                text_content = text_content.replace('<h2>', '## ').replace('</h2>', '\n')
                text_content = text_content.replace('<h3>', '### ').replace('</h3>', '\n')
                text_content = text_content.replace('<p>', '').replace('</p>', '\n')
                text_content = text_content.replace('<ul>', '').replace('</ul>', '\n')
                text_content = text_content.replace('<li>', '- ').replace('</li>', '\n')
                text_content = text_content.replace('<strong>', '**').replace('</strong>', '**')
                text_content = text_content.replace('<em>', '*').replace('</em>', '*')
                
                # Split into chunks
                chunks = self.text_splitter.split_text(text_content)
                
                # Create documents with metadata
                for i, chunk in enumerate(chunks):
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": md_file.name,
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                            "file_type": "markdown"
                        }
                    )
                    documents.append(doc)
            
            # Add documents to vector store
            if documents:
                vectorstore.add_documents(documents)
                print(f"Successfully embedded {len(documents)} chunks from {len(list(docs_path.glob('*.md')))} files")
                return True
            else:
                print("No documents found to embed")
                return False
                
        except Exception as e:
            print(f"Error embedding documents: {str(e)}")
            return False
    
    def build_support_qa(self, collection_name: str = "support_docs") -> RetrievalQA:
        """
        Build a RetrievalQA chain for support queries
        
        Args:
            collection_name: Name of the vector collection to use
            
        Returns:
            RetrievalQA: Configured QA chain
        """
        try:
            # Create vector store connection
            connection_string = f"postgresql+psycopg2://{settings.DATABASE_URL.split('://')[1]}"
            vectorstore = PGVector(
                collection_name=collection_name,
                connection_string=connection_string,
                embedding_function=self.embeddings
            )
            
            # Create retriever
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}
            )
            
            # Create LLM
            llm = ChatOpenAI(
                model_name="gpt-4o-mini",
                temperature=0.1,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Create QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": self._get_qa_prompt()
                }
            )
            
            return qa_chain
            
        except Exception as e:
            print(f"Error building support QA chain: {str(e)}")
            raise
    
    def _get_qa_prompt(self) -> str:
        """Get the prompt template for QA responses"""
        return """
        You are a helpful support assistant for the UC Berkeley Rideshare service. 
        Answer questions based on the provided documentation context.
        
        Guidelines:
        - Always base your answers on the provided context
        - Be helpful, accurate, and professional
        - If you don't have enough context, say so
        - Cite specific sections when possible
        - Keep responses concise but informative
        - Use a friendly, campus-appropriate tone
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
    
    def query_support(self, question: str, collection_name: str = "support_docs") -> Dict[str, Any]:
        """
        Query the support system with a user question
        
        Args:
            question: User's question
            collection_name: Name of the vector collection to use
            
        Returns:
            Dict containing answer and sources
        """
        try:
            qa_chain = self.build_support_qa(collection_name)
            
            # Get response
            result = qa_chain({"query": question})
            
            # Extract sources
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    sources.append({
                        "file": doc.metadata.get("source", "Unknown"),
                        "chunk": doc.metadata.get("chunk_index", 0)
                    })
            
            return {
                "answer": result["result"],
                "sources": sources,
                "question": question
            }
            
        except Exception as e:
            return {
                "answer": f"I'm sorry, I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "question": question,
                "error": True
            }

# Global instance
rag_service = RAGService()
