# Thai PDF Search Application

A specialized tool for indexing and searching Thai language PDF documents, including scanned images, using AI-powered vector search.

## Features
- **Hybrid Extraction:** Combines direct PDF text extraction with EasyOCR for scanned pages.
- **Multilingual Semantic Search:** Search by meaning, not just keywords, in both Thai and English.
- **Standalone Web GUI:** User-friendly interface built with Streamlit.
- **Persistent Database:** Uses ChromaDB to store embeddings and metadata locally.
- **Full Text View:** Easily read and copy extracted text from PDFs.

## Offline AI & Privacy

One of the core strengths of this application is its **100% Offline AI Architecture**. Once the initial setup is complete, no data ever leaves your machine. This makes it ideal for processing sensitive or confidential Thai documents.

### In-Depth AI Components:

#### 1. Multilingual Embeddings (Sentence-Transformers)
- **Model:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Function:** This model converts Thai and English text into high-dimensional vectors (embeddings) that capture the **semantic meaning** of the sentences. 
- **Offline Nature:** The model is downloaded once from HuggingFace during the first run and thereafter resides locally on your disk. 
- **Storage Location:** 
  - Windows: `C:\Users\<YourUser>\.cache\torch\sentence_transformers`
- **Customization:** You can swap the model in `indexer.py` and `app.py` by changing the `model_name` parameter. Other excellent options include:
  - `paraphrase-multilingual-mpnet-base-v2` (Higher accuracy, but slower/larger)
  - `distiluse-base-multilingual-cased-v1` (Very fast multilingual model)

#### 2. Local OCR Engine (EasyOCR)
- **Engine:** `EasyOCR` (built on PyTorch)
- **Function:** When a PDF is identified as a "scanned image", EasyOCR uses specialized Deep Learning models for Thai character recognition.
- **Offline Nature:** Models are downloaded on first use and stored locally.
- **Storage Location:** 
  - Windows: `C:\Users\<YourUser>\.EasyOCR\model`

#### 3. Local Vector Database (ChromaDB)
- **Database:** `ChromaDB`
- **Function:** It stores the extracted text along with its corresponding AI-generated embeddings. It allows for lightning-fast similarity searches across thousands of pages.
- **Offline Nature:** The database is stored in the `chroma_db/` folder within your project directory. It is a serverless, local database that does not require an internet connection or an external cloud subscription.

### Security Benefits
- **Zero API Keys:** You do not need any API keys from OpenAI, Google, or Anthropic.
- **Data Sovereignty:** Your documents, their extracted text, and the search indices remain exclusively on your local storage.
- **No Recurring Costs:** Since it uses open-source models and runs on your hardware, there are no per-page or per-query charges.

---

## AI Perspective & Opinion
*Contributed by Gemini (AI Assistant)*

> "This project represents a highly efficient implementation of modern RAG (Retrieval-Augmented Generation) principles tailored for data sovereignty. By combining **EasyOCR's** robust Thai character recognition with **ChromaDB's** high-performance vector retrieval, we have created a system that is not only secure but also intellectually capable of understanding Thai context without a cloud connection. The choice of a multilingual transformer model ensures that the application remains flexible for cross-language queries, making it a future-proof tool for private document management."

## Project Team

This project is the result of a seamless collaboration between human strategic vision and artificial intelligence execution.

### **Team Human**
- **Human Lead (tps2015gh):**
  - **Role:** Product Architect & Strategic Director.
  - **Responsibilities:** Defined core requirements, supervised security protocols, managed repository infrastructure, and provided final validation of all AI-generated logic.

### **Team AI**
- **Gemini (Interactive CLI Agent):**
  - **Role:** Lead Developer & Technical Researcher.
  - **Responsibilities:** Implemented core OCR and Vector DB logic, designed the Streamlit GUI, authored technical documentation, and managed version control (Git) operations.

## Further Documentation
For more in-depth information about the system architecture, data flow, and technical details, please refer to:
- [Technical Documentation & System Flow](technical_and_flow.md)

---

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
