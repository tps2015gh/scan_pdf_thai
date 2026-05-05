# Technical Documentation & System Flow

## 1. System Architecture
The system follows a Pipeline-Search-UI architecture:

### A. Data Ingestion (Indexer)
1.  **File Discovery:** Scans `data_files/` for `.pdf` files.
2.  **Deduplication:** Calculates MD5 hashes of files to avoid re-indexing unchanged documents.
3.  **Extraction Pipeline:**
    *   **Phase 1 (Direct):** Uses PyMuPDF (`fitz`) to attempt direct text extraction.
    *   **Phase 2 (OCR Fallback):** If extracted text is below a threshold (scanned document detection), it converts PDF pages to images and runs `EasyOCR`.
4.  **Vectorization:** Uses `paraphrase-multilingual-MiniLM-L12-v2` from Sentence-Transformers to create 384-dimensional embeddings.
5.  **Storage:** Saves embeddings, text content, and metadata (filename, page number, char/line counts) into `ChromaDB`.

### B. Search Engine
1.  **Query Processing:** The user's search string is converted into a vector using the same multilingual model.
2.  **Similarity Search:** Performs a K-Nearest Neighbors (KNN) search in ChromaDB using Cosine Similarity.
3.  **Metadata Retrieval:** Returns the most relevant page chunks with their associated file paths and statistics.

### C. Frontend (Streamlit)
1.  **Dashboard:** Aggregates metadata from ChromaDB to show library statistics.
2.  **Search Interface:** Captures user input and displays ranked results.
3.  **PDF Viewing:** 
    *   Embeds the PDF in an iframe for visual inspection.
    *   Retrieves all page chunks for a selected file to provide a "Full Text" copyable view.

## 2. Data Flow Diagram
```text
[PDF Files] -> [Indexer.py] -> [OCR/Extraction] -> [Embedding Model] -> [ChromaDB]
                                                                          |
[User Query] -> [App.py] -> [Embedding Model] -> [Similarity Search] <----+
                                                      |
                                             [Ranked Results & PDF View]
```

## 3. Technology Stack
- **PDF Processing:** PyMuPDF (fitz), pdfplumber
- **OCR:** EasyOCR (PyTorch based)
- **Vector DB:** ChromaDB
- **Embeddings:** Sentence-Transformers (HuggingFace)
- **Frontend:** Streamlit
- **Language:** Python 3.12

## 4. Understanding "Embedded" AI in this Project

There are two distinct ways the term "Embedded" applies to this project:

### A. Vector Embeddings (The Algorithm)
"Embeddings" refers to the process of turning Thai text into mathematical vectors. Instead of storing text as strings, we store them as points in a 384-dimensional space. The distance between these points represents the similarity in meaning.

### B. Local AI vs. Centralized Cache (The Storage)
While the AI runs **100% locally** (Edge/Embedded AI), you will not see the large AI model files (.bin, .safetensors) inside the project directory.

**Why are they not in the project folder?**
1.  **Shared Resources:** Python's AI libraries (`torch`, `transformers`) use a central cache folder (usually `~/.cache/`) to store models. This allows multiple projects to share the same model files without wasting disk space.
2.  **Git Best Practices:** Large binary files (1GB+) should not be committed to Git. The code is designed to automatically verify and load the model from the local cache.
3.  **Portability:** By keeping the logic (code) and data (ChromaDB) separate from the heavy AI models, the project remains lightweight and easy to manage.

**Result:** The project is **Offline** because the computation happens on your CPU/GPU, but the **Model Storage** is managed by the system-wide Python environment for efficiency.
