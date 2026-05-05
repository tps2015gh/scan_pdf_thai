# Thai PDF Search Application

A specialized tool for indexing and searching Thai language PDF documents, including scanned images, using AI-powered vector search.

## Features
- **Hybrid Extraction:** Combines direct PDF text extraction with EasyOCR for scanned pages.
- **Multilingual Semantic Search:** Search by meaning, not just keywords, in both Thai and English.
- **Standalone Web GUI:** User-friendly interface built with Streamlit.
- **Persistent Database:** Uses ChromaDB to store embeddings and metadata locally.
- **Full Text View:** Easily read and copy extracted text from PDFs.

## Windows Installation & Setup Guide

Follow these steps to set up the application on a Windows machine:

### 1. Prerequisites
- **Python 3.10+**: Download and install from [python.org](https://www.python.org/downloads/windows/). 
  - **Important:** Check the box **"Add Python to PATH"** during installation.

### 2. Clone or Download
Download this repository to your local machine (e.g., `C:\dev2\scan_pdf_thai`).

### 3. Setup Virtual Environment (Recommended)
Open PowerShell in the project directory and run:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies
Install all required Python components:
```powershell
pip install pdfplumber chromadb streamlit sentence-transformers pymupdf easyocr torch torchvision
```

### 5. Initialize the Database
Place your PDF files in the `data_files/` folder. Then, run the indexing script to scan and extract text:
```powershell
python indexer.py
```
*Note: The first run will download necessary AI models (~1GB).*

### 6. Launch the Application
You can start the web interface using the batch file or the command line:
- **Option A:** Double-click `run_app.bat`
- **Option B:** Run `streamlit run app.py`

## Project Structure
- `app.py`: Main Streamlit application.
- `indexer.py`: Script to process PDFs and populate the vector database.
- `data_files/`: Folder where you place your PDF documents.
- `chroma_db/`: Directory containing the indexed data and embeddings.
- `run_app.bat`: Quick launch script for Windows users.

## Requirements
- **Memory:** 4GB+ RAM recommended (EasyOCR and Embeddings are memory-intensive).
- **Disk:** ~2GB for library dependencies and AI models.
- **GPU (Optional):** If you have an NVIDIA GPU, installing CUDA will significantly speed up OCR.
