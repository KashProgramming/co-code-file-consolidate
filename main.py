import streamlit as st
import os
from file_handler.pdf_handler import extract_pdf_content
from file_handler.docx_handler import extract_docx_content
from file_handler.ppt_handler import extract_pptx_content
from content_processor.summarizer import summarize_content
from export_handler import export_images_and_text_to_docx, export_tables_to_docx

def process_files(uploaded_files):
    all_content = {"text": [], "tables": [], "images": []}
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        file_path = f"./uploaded_files/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        if uploaded_file.name.endswith(".pdf"):
            content = extract_pdf_content(file_path)
        elif uploaded_file.name.endswith(".docx"):
            content = extract_docx_content(file_path)
        elif uploaded_file.name.endswith(".pptx"):
            content = extract_pptx_content(file_path)
        else:
            st.warning(f"Unsupported file type: {uploaded_file.name}")
            continue
        # Append extracted content
        all_content["text"].extend(content["text"])
        all_content["tables"].extend(content["tables"])
        all_content["images"].extend(content["images"])
    all_content["text"] = summarize_content(all_content["text"])
    # Exporting documents
    export_images_and_text_to_docx(all_content)
    export_tables_to_docx(all_content)
    # Prepare downloadable links
    image_and_text_docx = "./output_images_and_text.docx"
    tables_docx = "./output_tables.docx"
    return image_and_text_docx, tables_docx

def main():
    st.title("File Processing and Summarization Tool")
    st.markdown("Upload a folder containing your files (PDF, DOCX, PPTX), and get a summarized document with relevant images, tables, and text.")
    # File uploader
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "pptx"], accept_multiple_files=True)
    if uploaded_files:
        st.write("Processing files...")
        # Process the files
        image_and_text_docx, tables_docx = process_files(uploaded_files)
        # Provide download links
        with open(image_and_text_docx, "rb") as f:
            st.download_button(
                label="Download Document with Images and Text",
                data=f,
                file_name="output_images_and_text.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        with open(tables_docx, "rb") as f:
            st.download_button(
                label="Download Document with Tables",
                data=f,
                file_name="output_tables.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    main()
