# Quick Setup Guide

## System Status

✅ **Document Processing**: Working perfectly with Docling  
✅ **Vector Database**: Milvus working with embeddings  
✅ **Document Retrieval**: Semantic search fully functional  
⚠️ **LLM Generation**: Requires HuggingFace API token

## Quick Start

### 1. Install Dependencies (Already Done)
```bash
uv sync
```

### 2. Build the Index
```bash
python main.py build
```

This will:
- Scan all documents in `./data/` directory
- Process them with Docling (supports PDF, DOCX, PPTX, HTML, MD, etc.)
- Create vector embeddings using sentence-transformers
- Store in Milvus vector database at `./.vectordb/`

### 3. Test Retrieval (Works Without API Token)
```bash
python test_retrieval.py
```

This demonstrates the semantic search capability by finding relevant document chunks for test queries.

### 4. Full RAG with LLM (Requires HuggingFace Token)

To use the complete RAG system with answer generation:

1. Get your free HuggingFace API token:
   - Visit: https://huggingface.co/settings/tokens
   - Create a new token (read access is sufficient)

2. Add to `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add: HF_TOKEN=your_token_here
   ```

3. Query with LLM:
   ```bash
   python main.py query -q "What is this document about?"
   ```

4. Interactive mode:
   ```bash
   python main.py interactive
   ```

## What's Working Now

### Document Loading ✅
- Scans `/data` directory
- Processes PDF files with advanced layout analysis
- Creates semantic chunks using HybridChunker
- Successfully loaded 9 chunks from PDF document

### Vector Search ✅
- Embeddings created with `sentence-transformers/all-MiniLM-L6-v2`
- Milvus vector database operational
- Semantic similarity search working perfectly
- Returns most relevant document chunks for queries

### Example Retrieval Results

Query: "Tell me about the visa"
- Found relevant chunks about e-Visa application status
- Retrieved applicant details and visa information
- Identified visa type, validity, and duration of stay

## Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Document Sources                         │
│              (PDF, DOCX, PPTX, HTML, MD, etc.)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Docling Processing                         │
│  • Layout Analysis (DocLayNet)                              │
│  • Table Recognition (TableFormer)                          │
│  • HybridChunker for semantic splitting                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Vector Embeddings Generation                    │
│          (sentence-transformers/all-MiniLM-L6-v2)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Milvus Vector Database                      │
│                  (Persistent storage)                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Semantic Search Layer                       │
│              (Cosine Similarity Retrieval)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   RAG Pipeline (Optional)                    │
│         LLM: mistralai/Mixtral-8x7B-Instruct-v0.1          │
│              (Requires HuggingFace Token)                   │
└─────────────────────────────────────────────────────────────┘
```

## Production Features

- ✅ Comprehensive error handling and logging
- ✅ Configurable via environment variables
- ✅ Persistent vector database (no rebuild needed)
- ✅ Multiple operation modes (build, query, interactive)
- ✅ Batch document processing with progress tracking
- ✅ Source attribution in results
- ✅ Fallback mechanisms for missing dependencies

## Next Steps

1. **Add HuggingFace token** to enable LLM answer generation
2. **Add more documents** to the `/data` directory
3. **Rebuild index** with `python main.py build --rebuild`
4. **Query your documents** with natural language questions

## Troubleshooting

### Documents Not Loading
- Check file format is supported (PDF, DOCX, PPTX, HTML, MD)
- TXT files need special handling (convert to .md)
- Check logs for specific errors

### Slow First Run
- First run downloads ML models (~100MB)
- Subsequent runs will be much faster
- Models are cached locally

### Out of Memory
- Reduce `CHUNK_SIZE` in `.env`
- Process fewer documents at once
- Use smaller embedding model

## Performance Notes

Current system processed:
- 1 PDF document (154KB)
- 9 semantic chunks created
- ~6 seconds total processing time
- Vector database: ~1MB
- Embedding model: ~90MB (cached)

## File Structure

```
docusearch/
├── data/                          # Your documents here
├── .vectordb/                     # Vector database (auto-created)
├── src/
│   ├── config.py                 # Configuration
│   ├── utils/logger.py           # Logging
│   └── rag/
│       ├── document_loader.py    # Document processing
│       ├── vector_store.py       # Vector database
│       └── rag.py                # RAG pipeline
├── main.py                       # CLI application
├── test_retrieval.py             # Test script
└── .env                          # Configuration (create from .env.example)
```
