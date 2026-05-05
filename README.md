# Thai PDF Search Application

A specialized tool for indexing and searching Thai language PDF documents, including scanned images, using AI-powered vector search.

## Features
- **Hybrid Extraction:** Combines direct PDF text extraction with EasyOCR for scanned pages.
- **Multilingual Semantic Search:** Search by meaning, not just keywords, in both Thai and English.
- **Standalone Web GUI:** User-friendly interface built with Streamlit.
- **Persistent Database:** Uses ChromaDB to store embeddings and metadata locally.
- **Full Text View:** Easily read and copy extracted text from PDFs.

## Project Structure
- `app.py`: Main Streamlit application.
- `indexer.py`: Script to process PDFs and populate the vector database.
- `data_files/`: Folder where you place your PDF documents.
- `chroma_db/`: Directory containing the indexed data and embeddings.
- `run_app.bat`: Quick launch script for Windows users.

## Requirements
- Python 3.10 or higher
- Tesseract OCR (Optional, EasyOCR is used by default)
- 4GB+ RAM recommended for OCR processing
