"""Test script to verify document retrieval works without LLM."""
from src.rag.vector_store import VectorStoreManager
from src.utils import get_logger

logger = get_logger(__name__)


def test_retrieval():
    """Test document retrieval functionality."""
    print("=" * 80)
    print("Testing Document Retrieval")
    print("=" * 80)

    # Load vector store
    logger.info("Loading vector store...")
    vector_store = VectorStoreManager()
    vector_store.load_vectorstore()

    # Test queries
    test_queries = [
        "What information is in the document?",
        "Tell me about the visa",
        "What are the key details?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 80)

        # Perform similarity search
        results = vector_store.similarity_search(query, k=3)

        print(f"Found {len(results)} relevant chunks:\n")

        for i, doc in enumerate(results, 1):
            print(f"[{i}] Source: {doc.metadata.get('source_file', 'Unknown')}")
            print(f"    Content: {doc.page_content[:300]}...")
            print()

    print("=" * 80)
    print("Retrieval test completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    test_retrieval()
