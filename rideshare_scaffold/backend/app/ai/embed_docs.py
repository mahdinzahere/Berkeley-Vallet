#!/usr/bin/env python3
"""
Script to embed documentation files for the RAG pipeline
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.ai.rag import rag_service

def main():
    """Main function to embed documentation"""
    
    # Get the docs path (relative to this script)
    script_dir = Path(__file__).parent
    docs_path = script_dir.parent / "docs"
    
    print(f"Starting document embedding process...")
    print(f"Documentation path: {docs_path}")
    
    # Check if docs directory exists
    if not docs_path.exists():
        print(f"Error: Documentation directory not found at {docs_path}")
        sys.exit(1)
    
    # Check if we have the required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    if not os.getenv("DATABASE_URL"):
        print("Error: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    # Check if pgvector extension is available
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Test database connection
        db_url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Check if pgvector extension exists
        cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        if not cursor.fetchone():
            print("Error: pgvector extension not installed in PostgreSQL")
            print("Please install pgvector extension first:")
            print("  CREATE EXTENSION vector;")
            conn.close()
            sys.exit(1)
        
        conn.close()
        print("✓ Database connection and pgvector extension verified")
        
    except ImportError:
        print("Error: psycopg2 not installed")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        sys.exit(1)
    
    # Start embedding process
    print("\nStarting document embedding...")
    
    try:
        success = rag_service.embed_docs(
            docs_path=str(docs_path),
            collection_name="support_docs"
        )
        
        if success:
            print("\n✓ Document embedding completed successfully!")
            print("The RAG pipeline is now ready to answer support questions.")
        else:
            print("\n✗ Document embedding failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Error during document embedding: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
