"""Document loader for scanning and loading documents from the data directory."""
from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from docling.chunking import HybridChunker

from src.config import Config
from src.utils import get_logger

logger = get_logger(__name__)


class DocumentScanner:
    """Scans and loads documents from a directory using Docling."""

    def __init__(
        self,
        data_dir: Optional[Path] = None,
        export_type: ExportType = ExportType.DOC_CHUNKS,
    ):
        """Initialize the document scanner.

        Args:
            data_dir: Directory containing documents to scan
            export_type: Type of export for document processing
        """
        self.data_dir = data_dir or Config.DATA_DIR
        self.export_type = export_type
        self.chunker = HybridChunker(tokenizer=Config.EMBED_MODEL_ID)

        if not self.data_dir.exists():
            raise ValueError(f"Data directory does not exist: {self.data_dir}")

    def scan_documents(self) -> List[Path]:
        """Scan the data directory for supported documents.

        Returns:
            List of document file paths
        """
        documents = []

        logger.info(f"Scanning directory: {self.data_dir}")

        for file_path in self.data_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in Config.SUPPORTED_EXTENSIONS:
                documents.append(file_path)
                logger.info(f"Found document: {file_path.name}")

        logger.info(f"Total documents found: {len(documents)}")
        return documents

    def load_document(self, file_path: Path) -> List[Document]:
        """Load a single document using Docling.

        Args:
            file_path: Path to the document

        Returns:
            List of document chunks
        """
        try:
            logger.info(f"Loading document: {file_path.name}")

            loader = DoclingLoader(
                file_path=str(file_path),
                export_type=self.export_type,
                chunker=self.chunker,
            )

            docs = loader.load()
            logger.info(f"Loaded {len(docs)} chunks from {file_path.name}")

            # Add source metadata
            for doc in docs:
                doc.metadata["source_file"] = file_path.name
                doc.metadata["source_path"] = str(file_path)

            return docs

        except Exception as e:
            logger.error(f"Failed to load document {file_path.name}: {str(e)}")
            raise

    def load_all_documents(self, file_paths: Optional[List[Path]] = None) -> List[Document]:
        """Load all documents from the data directory.

        Args:
            file_paths: Optional list of specific file paths to load

        Returns:
            List of all document chunks
        """
        if file_paths is None:
            file_paths = self.scan_documents()

        if not file_paths:
            logger.warning("No documents found to load")
            return []

        all_docs = []
        failed_files = []

        for file_path in file_paths:
            try:
                docs = self.load_document(file_path)
                all_docs.extend(docs)
            except Exception as e:
                logger.error(f"Skipping {file_path.name} due to error: {str(e)}")
                failed_files.append(file_path.name)

        logger.info(f"Successfully loaded {len(all_docs)} total chunks from {len(file_paths) - len(failed_files)} documents")

        if failed_files:
            logger.warning(f"Failed to load {len(failed_files)} documents: {', '.join(failed_files)}")

        return all_docs


def load_documents_from_directory(data_dir: Optional[Path] = None) -> List[Document]:
    """Convenience function to load all documents from a directory.

    Args:
        data_dir: Directory containing documents

    Returns:
        List of document chunks
    """
    scanner = DocumentScanner(data_dir=data_dir)
    return scanner.load_all_documents()
