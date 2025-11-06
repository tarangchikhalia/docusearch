"""CLI functions for the document RAG system."""
import sys
from pathlib import Path
from typing import Optional

from src.config import Config
from src.utils import get_logger
from src.rag.document_loader import DocumentScanner
from src.rag.vector_store import VectorStoreManager
from src.rag.rag import RAGPipeline

logger = get_logger(__name__)


def build_index(data_dir: Optional[Path] = None, force_rebuild: bool = False) -> VectorStoreManager:
    """Build or rebuild the document index.

    Args:
        data_dir: Directory containing documents
        force_rebuild: Whether to rebuild the index even if it exists

    Returns:
        Initialized VectorStoreManager
    """
    logger.info("=" * 80)
    logger.info("Building Document Index")
    logger.info("=" * 80)

    # Ensure data_dir exists
    if data_dir is not None:
        Config.DATA_DIR = data_dir
    
    # Ensure directories exist
    Config.ensure_directories()
    
    # Load documents
    logger.info("Step 1: Loading documents from directory")
    scanner = DocumentScanner(data_dir=data_dir)
    documents = scanner.load_all_documents()

    if not documents:
        logger.error("No documents found or loaded. Please add documents to the data directory.")
        sys.exit(1)

    logger.info(f"Successfully loaded {len(documents)} document chunks")

    # Create vector store
    logger.info("Step 2: Creating vector store and embeddings")
    vector_store_manager = VectorStoreManager()
    vector_store_manager.create_vectorstore(documents, drop_old=force_rebuild)

    logger.info("=" * 80)
    logger.info("Index built successfully!")
    logger.info("=" * 80)

    return vector_store_manager


def query_documents(question: str, load_existing: bool = True) -> dict:
    """Query the document index.

    Args:
        question: Question to ask
        load_existing: Whether to load existing index

    Returns:
        Query result dictionary
    """
    logger.info("=" * 80)
    logger.info("Querying Document Index")
    logger.info("=" * 80)

    # Load or build index
    vector_store_manager = VectorStoreManager()

    if load_existing:
        try:
            logger.info("Loading existing vector store")
            vector_store_manager.load_vectorstore()
        except Exception as e:
            logger.warning(f"Failed to load existing index: {str(e)}")
            logger.info("Building new index...")
            vector_store_manager = build_index()
    else:
        vector_store_manager = build_index()

    # Create RAG pipeline
    logger.info("Initializing RAG pipeline")
    rag = RAGPipeline(vector_store_manager)

    # Query
    logger.info(f"Question: {question}")
    result = rag.query(question)

    return result


def interactive_mode():
    """Run in interactive query mode."""
    logger.info("=" * 80)
    logger.info("Interactive RAG Query Mode")
    logger.info("=" * 80)
    logger.info("Type 'exit' or 'quit' to exit")
    logger.info("Type 'rebuild' to rebuild the index")
    logger.info("=" * 80)

    # Load vector store
    vector_store_manager = VectorStoreManager()
    try:
        vector_store_manager.load_vectorstore()
        logger.info("Loaded existing vector store")
    except Exception as e:
        logger.info(f"No existing index found. Building new index...")
        vector_store_manager = build_index()

    # Create RAG pipeline
    rag = RAGPipeline(vector_store_manager)

    while True:
        try:
            question = input("\nYour question: ").strip()

            if question.lower() in ["exit", "quit"]:
                logger.info("Exiting...")
                break

            if question.lower() == "rebuild":
                logger.info("Rebuilding index...")
                vector_store_manager = build_index(force_rebuild=True)
                rag = RAGPipeline(vector_store_manager)
                continue

            if not question:
                continue

            result = rag.query(question)

            print("\n" + "=" * 80)
            print(f"Question: {result['question']}")
            print("=" * 80)
            print(f"Answer: {result['answer']}")
            print("=" * 80)

            if "sources" in result:
                print(f"\nSources ({result['num_sources']} documents):")
                for source in result["sources"]:
                    print(f"\n[{source['number']}] {source['metadata'].get('source_file', 'Unknown')}")
                    print(f"    {source['content'][:200]}...")

        except KeyboardInterrupt:
            logger.info("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
