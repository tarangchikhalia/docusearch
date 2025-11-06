"""Configuration management for the RAG system."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the RAG system."""

    # Directories
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    VECTOR_DB_DIR = PROJECT_ROOT / ".vectordb"

    # Model Configuration
    EMBED_MODEL_ID: str = os.getenv(
        "EMBED_MODEL_ID",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    GEN_MODEL_ID: str = os.getenv(
        "GEN_MODEL_ID",
        "google/flan-t5-large"  # Default to a model that supports text-generation task
    )

    # HuggingFace Token
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")

    # Vector Database Configuration
    MILVUS_COLLECTION_NAME: str = "docusearch_documents"
    MILVUS_INDEX_TYPE: str = "FLAT"

    # Chunking Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "128"))

    # Retrieval Configuration
    TOP_K: int = int(os.getenv("TOP_K", "5"))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # RAG Prompt Template
    RAG_PROMPT_TEMPLATE: str = """Context information is below.
---------------------
{context}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: {input}
Answer:"""

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        ".pdf", ".docx", ".doc", ".pptx", ".ppt",
        ".html", ".htm", ".txt", ".md"
    }

    # Disable tokenizers parallelism warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.VECTOR_DB_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)

    @classmethod
    def get_milvus_uri(cls) -> str:
        """Get Milvus database URI."""
        return str(cls.VECTOR_DB_DIR / "milvus.db")

    @classmethod
    def validate(cls) -> None:
        """Validate configuration."""
        if not cls.HF_TOKEN:
            print("WARNING: HF_TOKEN not set. LLM generation may not work.")
