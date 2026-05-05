# 🚀 Thai PDF Searcher - Quick Start

This application allows you to search through Thai PDF documents (including scanned ones) using Vector Search and OCR.

## Step 1: Install Dependencies
Ensure you have Python 3.10+ installed, then run:
```bash
pip install pdfplumber chromadb streamlit sentence-transformers pymupdf easyocr torch torchvision
```

## Step 2: Index your PDFs
Place your PDF files in the `data_files/` folder and run the indexer.
*(Note: Current files in data_files/ are already indexed in the provided chroma_db folder)*
```bash
python indexer.py
```

## Step 3: Launch the Search GUI
Start the web-based search interface:
```bash
streamlit run app.py
```
**Or simply double-click `run_app.bat`**

---
### Note
The first time you run `indexer.py` or `app.py`, it may download AI models (about 1GB total). This only happens once.
