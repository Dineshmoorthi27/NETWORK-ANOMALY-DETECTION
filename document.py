import streamlit as st

st.title("PDF Viewer")

# Replace 'google_drive_pdf_link' with the shareable link of your PDF file hosted on Google Drive
google_drive_pdf_link = "https://drive.google.com/file/d/1fQtxW8eM6p7SDWOlQxUS4DOzBJ6qWnjL/view?usp=sharing"

# Display the PDF file using Google Drive Viewer
st.markdown(f'<iframe src="https://drive.google.com/viewerng/viewer?embedded=true&url={google_drive_pdf_link}" width="700" height="500" frameborder="0"></iframe>', unsafe_allow_html=True)
