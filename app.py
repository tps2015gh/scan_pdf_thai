import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import os
import base64

# Page config
st.set_page_config(page_title="Thai PDF Searcher", layout="wide")

# Initialize ChromaDB
@st.cache_resource
def get_chroma_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    return client.get_collection(name="pdf_collection", embedding_function=embedding_model)

collection = get_chroma_collection()

def get_pdf_stats():
    # Fetch all metadata to calculate stats
    all_data = collection.get(include=['metadatas'])
    metadatas = all_data['metadatas']
    
    stats = {}
    for meta in metadatas:
        filename = meta['filename']
        if filename not in stats:
            stats[filename] = {"char_count": 0, "line_count": 0, "pages": 0}
        stats[filename]["char_count"] += meta['char_count']
        stats[filename]["line_count"] += meta['line_count']
        stats[filename]["pages"] += 1
    return stats

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Sidebar - Stats
st.sidebar.title("PDF Library Stats")
stats = get_pdf_stats()
st.sidebar.write(f"Total PDFs: {len(stats)}")

for filename, data in stats.items():
    with st.sidebar.expander(f"📄 {filename}"):
        st.write(f"Pages: {data['pages']}")
        st.write(f"Total Chars: {data['char_count']}")
        st.write(f"Total Lines: {data['line_count']}")

# Main UI
st.title("🔍 Thai PDF Searcher")

query = st.text_input("Enter search text (Thai or English):")

if query:
    results = collection.query(
        query_texts=[query],
        n_results=10,
        include=['documents', 'metadatas', 'distances']
    )
    
    if results['ids'] and len(results['ids'][0]) > 0:
        st.subheader(f"Search Results for: '{query}'")
        
        for i in range(len(results['ids'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            dist = results['distances'][0][i]
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {meta['filename']} (Page {meta['page_num']})")
                with col2:
                    st.write(f"Relevance: {1 - dist:.4f}")
                
                st.text_area("Extracted Text:", value=doc, height=150, key=f"text_{i}")
                
                if st.button(f"View Original PDF - {meta['filename']} (P. {meta['page_num']})", key=f"btn_{i}"):
                    st.session_state['view_file'] = meta['file_path']
                    st.session_state['view_page'] = meta['page_num']
                    st.rerun()
                st.divider()
    else:
        st.warning("No matches found.")

# View PDF Section
if 'view_file' in st.session_state:
    filename = os.path.basename(st.session_state['view_file'])
    st.header(f"Viewing: {filename}")
    
    if st.button("Close Viewer"):
        del st.session_state['view_file']
        st.rerun()
    
    tab1, tab2 = st.tabs(["📄 PDF Viewer", "📝 Full Text (Readable & Copyable)"])
    
    with tab1:
        display_pdf(st.session_state['view_file'])
    
    with tab2:
        # Get all text for this file from ChromaDB
        file_results = collection.get(
            where={"filename": filename},
            include=['documents', 'metadatas']
        )
        
        # Sort by page number
        sorted_pages = sorted(zip(file_results['metadatas'], file_results['documents']), key=lambda x: x[0]['page_num'])
        
        full_text = ""
        for meta, doc in sorted_pages:
            full_text += f"--- Page {meta['page_num']} ---\n{doc}\n\n"
        
        st.text_area("Full Extracted Text", value=full_text, height=600)
