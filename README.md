# DocuSearch - Document RAG System

A production-grade Retrieval-Augmented Generation (RAG) system built with Docling, LangChain, and Ollama for intelligent document search and question answering.

## Features

- **Advanced Document Processing**: Uses Docling with state-of-the-art AI models for layout analysis and table structure recognition
- **Hybrid Chunking**: Intelligent document chunking using HybridChunker for optimal retrieval
- **Vector Search**: Milvus vector database with HuggingFace embeddings for semantic search
- **Local LLM with Ollama**: Privacy-focused, fast local inference without API costs
- **RAG Pipeline**: Complete retrieval and generation pipeline with customizable prompts
- **Multiple Modes**: Build index, one-shot query, or interactive chat mode
- **Production Ready**: Comprehensive error handling, logging, and configuration management
- **Supported Formats**: PDF, DOCX, PPTX, HTML, TXT, MD, and more

## Architecture

```
docusearch/
├── src/
│   ├── config.py              # Central configuration management
│   ├── utils/
│   │   └── logger.py          # Logging utilities
│   └── rag/
│       ├── document_loader.py # Document scanning and loading
│       ├── vector_store.py    # Vector database management
│       ├── cli.py             # CLI functions
│       └── rag.py             # RAG query pipeline with Ollama
├── data/                      # Place your documents here
├── .vectordb/                 # Vector database storage (auto-created)
└── main.py                    # Application entry point
```

## Prerequisites

### 1. Install Ollama

Ollama runs LLMs locally on your machine. It's free, private, and doesn't require API keys.

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from [ollama.com](https://ollama.com)

**Verify installation:**
```bash
ollama --version
```

### 2. Pull an LLM Model

Pull a model to use with the RAG system:

```bash
# Recommended: Llama 3.2 (3B parameters, fast and accurate)
ollama pull llama3.2

# Alternative models:
ollama pull mistral        # Mistral 7B
ollama pull llama3.1       # Llama 3.1 8B
ollama pull phi3           # Microsoft Phi-3
ollama pull gemma2         # Google Gemma 2
```

**Start Ollama server** (if not auto-started):
```bash
ollama serve
```

## Installation

1. **Clone and setup the project**:
```bash
git clone https://github.com/tarangchikhalia/docusearch.git
cd docusearch
```

2. **Install dependencies**:
```bash
uv sync
# or
uv pip install -e .
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env to set your preferred Ollama model (default: llama3.2)
```

## Usage

### 1. Build the Document Index

```bash
python main.py build --data-dir <path_to_data_directory> [--rebuild]
```

Options:
- `--data-dir PATH`: Specify a custom data directory
- `--rebuild`: Force rebuild the index (optional)

### 2. Query Documents (One-shot)

Ask a single question:

```bash
python main.py query -q "What is the main topic of these documents?"
```

Options:
- `-q, --question`: Your question (required)
- `--rebuild`: Rebuild index before querying
- `--no-sources`: Don't show source documents

### 3. Interactive Mode

Start an interactive chat session:

```bash
python main.py interactive
```

In interactive mode:
- Type your questions and press Enter
- Type `rebuild` to rebuild the index
- Type `exit` or `quit` to exit

## Configuration

Edit `.env` to customize the system:

```env
# Model Configuration
EMBED_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2

# Ollama Configuration (local LLM)
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# Chunking Configuration
CHUNK_SIZE=512
CHUNK_OVERLAP=128

# Retrieval Configuration
TOP_K=5

# Logging
LOG_LEVEL=INFO
```

## Advanced Configuration

You can customize the system by modifying `src/config.py`:

- **Supported file extensions**: Add or remove file types
- **Prompt template**: Customize the RAG prompt
- **Vector database settings**: Change index type or collection name
- **Model parameters**: Adjust embedding model and Ollama settings

## Example Queries

```bash
# Build index
python main.py build

# Ask about specific content
python main.py query -q "What are the key findings in the research papers?"

# Ask for summaries
python main.py query -q "Summarize the main points from all documents"

# Ask about specific topics
python main.py query -q "What does the document say about machine learning?"

# Interactive mode for multiple questions
python main.py interactive
```

## How It Works

1. **Document Loading**: Scans the `data/` directory and processes documents using Docling's advanced converters
2. **Chunking**: Splits documents into semantically meaningful chunks using HybridChunker
3. **Embedding**: Converts chunks to vector embeddings using HuggingFace models
4. **Indexing**: Stores embeddings in Milvus vector database for efficient retrieval
5. **Retrieval**: Finds most relevant chunks based on semantic similarity to the query
6. **Generation**: Uses Ollama (local LLM) to generate answers based on retrieved context

## Supported Document Types

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`, `.ppt`)
- HTML (`.html`, `.htm`)
- Text files (`.txt`)
- Markdown (`.md`)

## Performance Tips

1. **Model Selection**: 
   - Small models (llama3.2, phi3): Faster, good for most use cases
   - Large models (llama3.1, gemma2): Better quality, slower

2. **GPU Acceleration**: Ollama automatically uses GPU if available

3. **Index Persistence**: The vector database is persisted to disk, so you only need to build once

4. **Batch Processing**: For large document sets, the system automatically processes documents in batches

## Troubleshooting

### Ollama Connection Error
**Error**: `Failed to initialize Ollama LLM`

**Solutions**:
1. Ensure Ollama is running: `ollama serve`
2. Check the model is pulled: `ollama list`
3. Verify the URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### Model Not Found
**Error**: `model 'llama3.2' not found`

**Solution**:
```bash
ollama pull llama3.2
```

### Documents Not Found
Ensure your documents are in the `data/` directory and have supported extensions.

### Out of Memory
Try:
1. Use a smaller model (e.g., `llama3.2` instead of `llama3.1`)
2. Reduce `CHUNK_SIZE` in `.env`
3. Close other applications

### Slow Processing
- First-time loading downloads models and may take time
- Subsequent runs will be faster
- Consider using a smaller model for faster responses

## Why Ollama?

- **Privacy**: All processing happens locally, your data never leaves your machine
- **Cost**: No API fees, unlimited usage
- **Speed**: Fast local inference, no network latency
- **Offline**: Works without internet connection
- **Quality**: Access to latest open-source models (Llama, Mistral, etc.)

## Dependencies

Key dependencies:
- `docling`: Advanced document processing
- `langchain`: RAG framework
- `langchain-ollama`: Ollama integration for LangChain
- `langchain-docling`: Docling integration for LangChain
- `langchain-milvus`: Milvus vector database integration
- `sentence-transformers`: Embedding models

See `pyproject.toml` for complete list.

## License

This project uses the following open-source libraries:
- Docling (MIT License)
- LangChain (MIT License)
- Ollama (MIT License)
- See individual package licenses for more details

## References

- [Ollama](https://ollama.com)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Milvus Documentation](https://milvus.io/docs)
