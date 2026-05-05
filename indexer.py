import os
import fitz
import easyocr
import numpy as np
from PIL import Image
import io
import chromadb
from chromadb.utils import embedding_functions
import hashlib

# Initialize EasyOCR reader
reader = easyocr.Reader(['th', 'en'])

# Initialize ChromaDB
client = chromadb.PersistentClient(path="chroma_db")
embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
collection = client.get_or_create_collection(name="pdf_collection", embedding_function=embedding_model)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def extract_text_from_pdf(file_path):
    print(f"Processing: {file_path}")
    doc = fitz.open(file_path)
    full_text = ""
    pages_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        
        # If direct extraction fails or yields very little text, try OCR
        if len(text.strip()) < 50:
            print(f"  Page {page_num+1}: Direct extraction yielded little text. Using OCR...")
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            img_np = np.array(img)
            results = reader.readtext(img_np, detail=0)
            text = "\n".join(results)
        
        full_text += text + "\n"
        pages_data.append({
            "page_num": page_num + 1,
            "text": text
        })
    
    doc.close()
    return full_text, pages_data

def index_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    
    for filename in pdf_files:
        file_path = os.path.join(directory, filename)
        file_id = get_file_hash(file_path)
        
        # Check if already indexed
        existing = collection.get(ids=[file_id])
        if existing['ids']:
            print(f"Skipping {filename}, already indexed.")
            continue
            
        text, pages = extract_text_from_pdf(file_path)
        
        # Split text into chunks for better search? 
        # For now, let's index page by page to keep metadata accurate
        for i, page in enumerate(pages):
            page_id = f"{file_id}_p{page['page_num']}"
            if not page['text'].strip():
                continue
                
            collection.add(
                ids=[page_id],
                documents=[page['text']],
                metadatas=[{
                    "filename": filename,
                    "page_num": page['page_num'],
                    "file_path": file_path,
                    "char_count": len(page['text']),
                    "line_count": len(page['text'].split('\n'))
                }]
            )
        print(f"Indexed {filename}")

if __name__ == "__main__":
    index_pdfs("data_files")
