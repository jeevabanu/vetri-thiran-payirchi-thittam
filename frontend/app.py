import os
import requests
import streamlit as st
from dotenv import load_dotenv
from formatter import format_txt, format_docx, format_pdf

load_dotenv()
BACKEND = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.title("⚖️ LegalEase: AI Legal Document Generator")

logo = st.sidebar.file_uploader("Company logo (optional)", type=["png", "jpg", "jpeg"])
logo_bytes = logo.read() if logo else None
if logo_bytes:
    st.sidebar.image(logo_bytes)

col1, col2 = st.columns(2)
with col1:
    doc_type = st.text_input("Document type", "Non-Disclosure Agreement")
    dates = st.text_input("Effective date(s)", "1 October 2026")
    parties = st.text_area("Parties involved", "Acme Pvt Ltd and John Doe")
    terms = st.text_area("Key terms", "Duration: 2 years\nGoverning law: India")

    if st.button("Generate Document", type="primary"):
        with st.spinner("Drafting your document..."):
            try:
                r = requests.post(
                    f"{BACKEND}/generate",
                    json={"document_type": doc_type, "parties": parties,
                          "terms": terms, "dates": dates},
                    timeout=120,
                )
                r.raise_for_status()
                st.session_state["doc"] = r.json()["document"]
            except Exception as e:
                st.error(f"Generation failed: {e}")

with col2:
    if "doc" in st.session_state:
        st.subheader("Editable preview")
        edited = st.text_area("Edit the document", st.session_state["doc"], height=500)
        st.session_state["doc"] = edited

        c1, c2, c3 = st.columns(3)
        c1.download_button("Download TXT", format_txt(edited, doc_type),
                           "document.txt", "text/plain")
        c2.download_button("Download DOCX", format_docx(edited, doc_type, logo_bytes),
                           "document.docx",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        c3.download_button("Download PDF", format_pdf(edited, doc_type, logo_bytes),
                           "document.pdf", "application/pdf")