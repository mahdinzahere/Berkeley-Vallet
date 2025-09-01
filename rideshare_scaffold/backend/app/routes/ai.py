from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ..ai.rag import rag_service

router = APIRouter(prefix="/ai", tags=["artificial intelligence"])

class SupportQuery(BaseModel):
    question: str
    user_id: Optional[int] = None
    context: Optional[str] = None

class SupportResponse(BaseModel):
    answer: str
    sources: List[dict]
    question: str
    error: Optional[bool] = False

@router.post("/support", response_model=SupportResponse)
async def get_support_answer(query: SupportQuery):
    """
    Get AI-powered support answer based on documentation
    
    This endpoint uses the RAG pipeline to provide intelligent,
    context-aware responses to user support questions.
    """
    try:
        # Validate input
        if not query.question or len(query.question.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        if len(query.question) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question too long (max 500 characters)"
            )
        
        # Get response from RAG service
        result = rag_service.query_support(
            question=query.question.strip(),
            collection_name="support_docs"
        )
        
        return SupportResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error in AI support endpoint: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your question. Please try again later."
        )

@router.get("/support/health")
async def support_health_check():
    """
    Health check for the AI support system
    
    This endpoint verifies that the RAG pipeline is working
    and can access the embedded documentation.
    """
    try:
        # Try to build the QA chain to verify everything is working
        qa_chain = rag_service.build_support_qa()
        
        # Test with a simple query
        test_result = rag_service.query_support(
            question="What is the base fare for rides?",
            collection_name="support_docs"
        )
        
        return {
            "status": "healthy",
            "message": "AI support system is operational",
            "test_query": "What is the base fare for rides?",
            "test_response_length": len(test_result.get("answer", "")),
            "sources_available": len(test_result.get("sources", []))
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"AI support system error: {str(e)}",
            "error": True
        }

@router.get("/support/examples")
async def get_support_examples():
    """
    Get example questions that the AI support system can answer
    
    This helps users understand what types of questions
    they can ask the support system.
    """
    examples = {
        "fare_questions": [
            "How much does a ride cost?",
            "What is the base fare?",
            "How are fares calculated?",
            "What's the per-mile rate?"
        ],
        "cancellation_policy": [
            "Can I cancel my ride?",
            "What are the cancellation fees?",
            "How do I cancel a ride?",
            "Is there a cancellation fee?"
        ],
        "campus_specific": [
            "Where are the best pickup spots on campus?",
            "What are peak hours?",
            "Where should I get picked up?",
            "What are the busiest times?"
        ],
        "safety_and_conduct": [
            "What are the safety features?",
            "How do I report a safety concern?",
            "What are the driver requirements?",
            "How do I stay safe during rides?"
        ],
        "payment_and_tips": [
            "What payment methods are accepted?",
            "How do I tip my driver?",
            "Do tips go directly to drivers?",
            "How do payments work?"
        ],
        "airport_runs": [
            "How much does it cost to go to the airport?",
            "What are the best routes to SFO?",
            "How long does it take to get to OAK?",
            "What are airport run best practices?"
        ]
    }
    
    return {
        "message": "Example questions for the AI support system",
        "categories": examples,
        "total_examples": sum(len(examples[cat]) for cat in examples)
    }
