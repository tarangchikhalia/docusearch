"""RAG query pipeline for document question answering."""
from typing import Optional, Dict, Any, List
from operator import itemgetter

from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_ollama import OllamaLLM

from src.config import Config
from src.utils import get_logger
from src.rag.vector_store import VectorStoreManager

logger = get_logger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline using Ollama."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager,
        model_name: Optional[str] = None,
        ollama_base_url: Optional[str] = None,
        prompt_template: Optional[str] = None,
        top_k: Optional[int] = None,
    ):
        """Initialize the RAG pipeline.

        Args:
            vector_store_manager: Initialized vector store manager
            model_name: Ollama model name (e.g., 'llama2', 'mistral')
            ollama_base_url: Ollama server URL (default: http://localhost:11434)
            prompt_template: Custom prompt template
            top_k: Number of documents to retrieve
        """
        self.vector_store_manager = vector_store_manager
        self.model_name = model_name or Config.OLLAMA_MODEL
        self.ollama_base_url = ollama_base_url or Config.OLLAMA_BASE_URL
        self.top_k = top_k or Config.TOP_K

        # Create prompt template
        template = prompt_template or Config.RAG_PROMPT_TEMPLATE
        self.prompt = PromptTemplate.from_template(template)

        # Initialize retriever
        self.retriever = self.vector_store_manager.get_retriever(top_k=self.top_k)

        # Initialize LLM
        self._init_llm()

        # Create RAG chain
        self._create_chain()

    def _init_llm(self) -> None:
        """Initialize the Ollama language model."""
        logger.info(f"Initializing Ollama LLM: {self.model_name}")
        logger.info(f"Ollama server URL: {self.ollama_base_url}")

        try:
            self.llm = OllamaLLM(
                model=self.model_name,
                base_url=self.ollama_base_url,
                temperature=0.7,
            )
            logger.info(f"Successfully initialized Ollama LLM: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama LLM: {str(e)}")
            logger.error("Make sure Ollama is running locally. Install it from: https://ollama.ai")
            logger.error(f"Then run: ollama pull {self.model_name}")
            raise

    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for the prompt."""
        return "\n\n".join(doc.page_content for doc in docs)

    def _create_chain(self) -> None:
        """Create the RAG chain using LCEL."""
        logger.info("Creating RAG chain using LCEL")

        try:
            # Create the RAG chain using LangChain Expression Language
            self.rag_chain = (
                RunnableParallel({
                    "context": itemgetter("input") | self.retriever | self._format_docs,
                    "input": itemgetter("input")
                })
                | self.prompt
                | self.llm
                | StrOutputParser()
            )

            logger.info("RAG chain created successfully")
        except Exception as e:
            logger.error(f"Failed to create RAG chain: {str(e)}")
            raise

    def query(self, question: str, return_sources: bool = True) -> Dict[str, Any]:
        """Query the RAG system.

        Args:
            question: User's question
            return_sources: Whether to return source documents

        Returns:
            Dictionary containing answer and optional source documents
        """
        logger.info(f"Processing query: '{question}'")

        try:
            # Get the answer
            answer = self.rag_chain.invoke({"input": question})

            result = {
                "question": question,
                "answer": answer,
            }

            # Get source documents if requested
            if return_sources:
                context_docs = self.retriever.invoke(question)
                result["sources"] = self._format_sources(context_docs)
                result["num_sources"] = len(context_docs)

            logger.info(f"Query processed successfully. Answer length: {len(result['answer'])} chars")
            return result

        except Exception as e:
            logger.error(f"Failed to process query: {str(e)}")
            raise

    def _format_sources(self, context_docs: List[Document]) -> List[Dict[str, Any]]:
        """Format source documents for output.

        Args:
            context_docs: List of context documents

        Returns:
            List of formatted source information
        """
        sources = []

        for i, doc in enumerate(context_docs, 1):
            source = {
                "number": i,
                "content": doc.page_content[:500],  # Limit content length
                "metadata": {
                    k: v for k, v in doc.metadata.items()
                    if k not in ["pk", "embedding"]  # Exclude technical metadata
                }
            }
            sources.append(source)

        return sources

    def batch_query(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Process multiple questions in batch.

        Args:
            questions: List of questions

        Returns:
            List of results for each question
        """
        logger.info(f"Processing batch of {len(questions)} questions")

        results = []
        for question in questions:
            try:
                result = self.query(question)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process question '{question}': {str(e)}")
                results.append({
                    "question": question,
                    "answer": f"Error: {str(e)}",
                    "error": True
                })

        return results


def create_rag_pipeline(vector_store_manager: VectorStoreManager) -> RAGPipeline:
    """Convenience function to create a RAG pipeline.

    Args:
        vector_store_manager: Initialized vector store manager

    Returns:
        RAG pipeline instance
    """
    return RAGPipeline(vector_store_manager)
