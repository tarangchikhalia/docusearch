# DocuSearch - Document RAG System

A production-grade Retrieval-Augmented Generation (RAG) system built with Docling and LangChain for intelligent document search and question answering.

## Features

- **Advanced Document Processing**: Uses Docling with state-of-the-art AI models for layout analysis and table structure recognition
- **Hybrid Chunking**: Intelligent document chunking using HybridChunker for optimal retrieval
- **Vector Search**: Milvus vector database with HuggingFace embeddings for semantic search
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
│       └── rag.py             # RAG query pipeline
├── data/                      # Place your documents here
├── .vectordb/                 # Vector database storage (auto-created)
└── main.py                    # Application entry point
```

## Installation

1. **Clone and setup the project**:
```bash
cd /Users/tarang/Developer/docusearch
```

2. **Install dependencies**:
```bash
uv sync
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env and add your HuggingFace token
```

Get your HuggingFace token from: https://huggingface.co/settings/tokens

## Usage

### 1. Build the Document Index

First, add your documents to the `data/` directory, then build the index:

```bash
python main.py build
```

Options:
- `--data-dir PATH`: Specify a custom data directory
- `--rebuild`: Force rebuild the index

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
# HuggingFace API Token (required)
HF_TOKEN=your_token_here

# Model Configuration
EMBED_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2
GEN_MODEL_ID=mistralai/Mixtral-8x7B-Instruct-v0.1

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
- **Model parameters**: Adjust embedding and generation models

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
6. **Generation**: Uses LLM to generate answers based on retrieved context

## Supported Document Types

- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Microsoft PowerPoint (`.pptx`, `.ppt`)
- HTML (`.html`, `.htm`)
- Text files (`.txt`)
- Markdown (`.md`)

## Performance Tips

1. **GPU Acceleration**: Set `device: 'cuda'` in `src/rag/vector_store.py` if you have a GPU
2. **Batch Processing**: For large document sets, the system automatically processes documents in batches
3. **Index Persistence**: The vector database is persisted to disk, so you only need to build once
4. **Model Selection**: Choose smaller models for faster processing or larger models for better accuracy

## Troubleshooting

### No HuggingFace Token
If you see "HF_TOKEN not provided" warning, the system will fall back to a simpler model. For best results, add your token to `.env`.

### Documents Not Found
Ensure your documents are in the `data/` directory and have supported extensions.

### Out of Memory
Try reducing `CHUNK_SIZE` or using a smaller embedding model.

### Slow Processing
First-time loading downloads models and may take time. Subsequent runs will be faster.

## Dependencies

Key dependencies:
- `docling`: Advanced document processing
- `langchain`: RAG framework
- `langchain-docling`: Docling integration for LangChain
- `langchain-huggingface`: HuggingFace model integration
- `langchain-milvus`: Milvus vector database integration
- `sentence-transformers`: Embedding models

See `pyproject.toml` for complete list.

## License

This project uses the following open-source libraries:
- Docling (MIT License)
- LangChain (MIT License)
- See individual package licenses for more details

## References

- [Docling Documentation](https://docling-project.github.io/docling/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Milvus Documentation](https://milvus.io/docs)
