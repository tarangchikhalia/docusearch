"""Vector store management for document embeddings."""
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain_core.vectorstores import VectorStoreRetriever

from src.config import Config
from src.utils import get_logger

logger = get_logger(__name__)


class VectorStoreManager:
    """Manages the vector store for document embeddings."""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        milvus_uri: Optional[str] = None,
        embed_model_id: Optional[str] = None,
    ):
        """Initialize the vector store manager.

        Args:
            collection_name: Name of the Milvus collection
            milvus_uri: URI for the Milvus database
            embed_model_id: ID of the embedding model to use
        """
        self.collection_name = collection_name or Config.MILVUS_COLLECTION_NAME
        self.milvus_uri = milvus_uri or Config.get_milvus_uri()
        self.embed_model_id = embed_model_id or Config.EMBED_MODEL_ID

        logger.info(f"Initializing embeddings with model: {self.embed_model_id}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embed_model_id,
            model_kwargs={'device': 'cpu'},  # Change to 'cuda' if GPU available
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vectorstore: Optional[Milvus] = None

    def create_vectorstore(
        self,
        documents: List[Document],
        drop_old: bool = True
    ) -> Milvus:
        """Create a new vector store from documents.

        Args:
            documents: List of documents to index
            drop_old: Whether to drop existing collection

        Returns:
            Milvus vector store instance
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")

        logger.info(f"Creating vector store with {len(documents)} documents")
        logger.info(f"Collection: {self.collection_name}")
        logger.info(f"Milvus URI: {self.milvus_uri}")

        try:
            self.vectorstore = Milvus.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                connection_args={"uri": self.milvus_uri},
                index_params={"index_type": Config.MILVUS_INDEX_TYPE},
                drop_old=drop_old,
            )

            logger.info("Vector store created successfully")
            return self.vectorstore

        except Exception as e:
            logger.error(f"Failed to create vector store: {str(e)}")
            raise

    def load_vectorstore(self) -> Milvus:
        """Load an existing vector store.

        Returns:
            Milvus vector store instance
        """
        logger.info(f"Loading existing vector store: {self.collection_name}")

        try:
            self.vectorstore = Milvus(
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
                connection_args={"uri": self.milvus_uri},
            )

            logger.info("Vector store loaded successfully")
            return self.vectorstore

        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            raise

    def get_retriever(
        self,
        top_k: Optional[int] = None,
        search_type: str = "similarity"
    ) -> VectorStoreRetriever:
        """Get a retriever from the vector store.

        Args:
            top_k: Number of documents to retrieve
            search_type: Type of search (similarity, mmr, etc.)

        Returns:
            Vector store retriever
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Call create_vectorstore or load_vectorstore first.")

        k = top_k or Config.TOP_K

        logger.info(f"Creating retriever with top_k={k}, search_type={search_type}")

        retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )

        return retriever

    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """Perform similarity search on the vector store.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        k = k or Config.TOP_K

        logger.info(f"Performing similarity search for: '{query}' (k={k})")

        results = self.vectorstore.similarity_search(query, k=k)
        logger.info(f"Found {len(results)} similar documents")

        return results

    def add_documents(self, documents: List[Document]) -> None:
        """Add new documents to the existing vector store.

        Args:
            documents: List of documents to add
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        if not documents:
            logger.warning("No documents provided to add")
            return

        logger.info(f"Adding {len(documents)} documents to vector store")

        try:
            self.vectorstore.add_documents(documents)
            logger.info("Documents added successfully")
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise

    def delete_collection(self) -> None:
        """Delete the vector store collection."""
        if self.vectorstore is None:
            logger.warning("No vector store to delete")
            return

        logger.info(f"Deleting collection: {self.collection_name}")

        try:
            self.vectorstore.col.drop()
            self.vectorstore = None
            logger.info("Collection deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete collection: {str(e)}")
            raise
