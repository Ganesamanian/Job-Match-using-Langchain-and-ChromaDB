import streamlit as st
from langchain_helper import process_data
import tempfile

st.title("Welcome to Job Match")
url = st.text_input("Copy paste the Job url here to find the match")
username = st.text_input("Enter your Github username")
vecdbname = st.text_input("Enter your vector database name to store your portfolio")
pdf_file = st.file_uploader("Upload Resume", type="pdf")

Match = st.button("Find Match")
if Match and pdf_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_pdf:
        tmp_pdf.write(pdf_file.read())  # Write the content of the uploaded file to the temp file
        tmp_pdf_path = tmp_pdf.name  # Get the path of the temporary file


    percent, relatedproject, resumetips, lettertips = process_data(username, url, tmp_pdf_path, vecdbname)
    
    # Display the percentage with a progress bar
    st.write(f"### Match Percentage: {percent}%")
    # Create a separator or heading for related projects

    # Add a heading separately before the expander
    st.markdown("## Related Projects")
    with st.expander("Expand to view projects", expanded=True):
        for idx, project in enumerate(relatedproject):
            st.write(f"##### {idx+1}. {project}")

    # Resume tips with heading and expander
    st.markdown("## Tips to Improve Your Resume")
    with st.expander("Expand to view tips", expanded=False):
        for idx, tips in enumerate(resumetips):
            st.write(f"{idx+1}. {tips}")
            if idx + 1 == 5:
                break

    # Cover letter tips with heading and expander
    st.markdown("## Tips to Write Your Cover Letter")
    with st.expander("Expand to view tips", expanded=False):
        for idx, tips in enumerate(lettertips):
            st.write(f"{idx+1}. {tips}")
            if idx + 1 == 5:
                break
    



