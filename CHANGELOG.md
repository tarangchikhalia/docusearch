# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-11-06

### Changed
- **BREAKING**: Migrated from HuggingFace to Ollama for LLM generation
  - Replaced `langchain-huggingface` dependency with `langchain-ollama`
  - Updated `src/rag/rag.py` to use `OllamaLLM` instead of `HuggingFaceEndpoint`
  - Refactored RAG chain to use LangChain Expression Language (LCEL)
  - Removed `HF_TOKEN` requirement from configuration
  - Added `OLLAMA_MODEL` and `OLLAMA_BASE_URL` configuration options
- Updated `.env.example` to remove HuggingFace token and add Ollama configuration
- Updated `README.md` with comprehensive Ollama setup instructions
  - Added Prerequisites section with Ollama installation instructions
  - Added model selection guide (llama3.2, mistral, llama3.1, phi3, gemma2)
  - Updated troubleshooting section with Ollama-specific help
  - Added "Why Ollama?" section highlighting privacy, cost, and speed benefits
- Updated `src/config.py` to use Ollama configuration instead of HuggingFace
- Relaxed `langchain-core` version constraint in `pyproject.toml` (removed upper bound)
- Added CLI functions module (`src/rag/cli.py`) to architecture diagram

### Added
- Ollama integration for local LLM inference
- Enhanced error handling for Ollama connection issues
- Better logging for Ollama initialization
- OLLAMA_MIGRATION.md documentation

### Removed
- HuggingFace API token requirement
- `langchain-huggingface` dependency
- `GEN_MODEL_ID` configuration option (replaced with `OLLAMA_MODEL`)

## [0.1-beta] - 2025-11-05

### Added
- Initial release of DocuSearch RAG system
- Advanced document processing using Docling with AI-powered layout analysis
- Hybrid chunking for intelligent document segmentation
- Milvus vector database integration for semantic search
- HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2)
- Complete RAG pipeline with customizable prompts
- CLI with three modes:
  - `build`: Build document index
  - `query`: One-shot question answering
  - `interactive`: Interactive chat mode
- Support for multiple document formats (PDF, DOCX, PPTX, HTML, TXT, MD)
- Production-ready error handling and logging
- Comprehensive documentation and examples

### Features
- Document loader with recursive directory scanning
- Vector store manager with Milvus Lite
- Configurable chunking parameters
- Top-K retrieval configuration
- Source document attribution
- Persistent vector database

### Dependencies
- docling >= 2.60.1
- langchain >= 0.3.0
- langchain-community >= 0.3.0
- langchain-core >= 0.3.0
- langchain-docling >= 1.1.0
- langchain-milvus >= 0.2.0
- langchain-text-splitters >= 0.3.0
- sentence-transformers >= 5.1.2
- tiktoken >= 0.12.0
- python-dotenv >= 1.0.0
- pymilvus[milvus_lite] >= 2.5.0

[Unreleased]: https://github.com/tarangchikhalia/docusearch/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/tarangchikhalia/docusearch/compare/v0.1-beta...v0.1.1
[0.1-beta]: https://github.com/tarangchikhalia/docusearch/releases/tag/v0.1-beta
