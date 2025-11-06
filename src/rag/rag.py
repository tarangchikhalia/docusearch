"""RAG query pipeline for document question answering."""
from typing import Optional, Dict, Any, List
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEndpoint

from src.config import Config
from src.utils import get_logger
from src.rag.vector_store import VectorStoreManager

logger = get_logger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(
        self,
        vector_store_manager: VectorStoreManager,
        gen_model_id: Optional[str] = None,
        hf_token: Optional[str] = None,
        prompt_template: Optional[str] = None,
        top_k: Optional[int] = None,
    ):
        """Initialize the RAG pipeline.

        Args:
            vector_store_manager: Initialized vector store manager
            gen_model_id: HuggingFace model ID for generation
            hf_token: HuggingFace API token
            prompt_template: Custom prompt template
            top_k: Number of documents to retrieve
        """
        self.vector_store_manager = vector_store_manager
        self.gen_model_id = gen_model_id or Config.GEN_MODEL_ID
        self.hf_token = hf_token or Config.HF_TOKEN
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
        """Initialize the language model."""
        if not self.hf_token:
            logger.warning("HF_TOKEN not provided. Using default model without authentication.")
            logger.warning("For better results, set HF_TOKEN environment variable.")

        logger.info(f"Initializing LLM: {self.gen_model_id}")

        # Prepare kwargs for HuggingFaceEndpoint
        llm_kwargs = {
            "repo_id": self.gen_model_id,
            "temperature": 0.7,
            "max_new_tokens": 512,
        }

        # Only add token if it's provided
        if self.hf_token:
            llm_kwargs["huggingfacehub_api_token"] = self.hf_token

        self.llm = HuggingFaceEndpoint(**llm_kwargs)
        logger.info(f"Successfully initialized LLM: {self.gen_model_id}")

    def _create_chain(self) -> None:
        """Create the RAG chain."""
        logger.info("Creating RAG chain")

        try:
            # Create document combination chain
            self.question_answer_chain = create_stuff_documents_chain(
                self.llm,
                self.prompt
            )

            # Create retrieval chain
            self.rag_chain = create_retrieval_chain(
                self.retriever,
                self.question_answer_chain
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
            # Invoke the RAG chain
            response = self.rag_chain.invoke({"input": question})

            result = {
                "question": response["input"],
                "answer": response["answer"],
            }

            if return_sources and "context" in response:
                result["sources"] = self._format_sources(response["context"])
                result["num_sources"] = len(response["context"])

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
