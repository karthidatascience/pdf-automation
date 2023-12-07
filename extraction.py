import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import os
import pandas as pd
import io
import zipfile


def extract_account_numbers(file_path, output_folder, df):
    inputpdf = PdfReader(open(file_path, "rb"))
    extracted_numbers = []

    for Pin, i in zip(df['Property Account No'], range(len(inputpdf.pages))):
        output = PdfWriter()
        output.add_page(inputpdf.pages[i])
        acc_num = f'{Pin}_Mail Out'
        output_file_path = os.path.join(output_folder, f"{acc_num}.pdf")
        with open(output_file_path, "wb") as outputStream:
            output.write(outputStream)
        extracted_numbers.append(output_file_path)

    return extracted_numbers


def main():
    st.title("PDF Account Number Extraction")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    uploaded_data = st.file_uploader("Upload a Pandas file", type=["csv", "xlsx"])

    output_folder = st.text_input("Enter the output folder name:", "Output_Folder_Name")

    if uploaded_file is not None and uploaded_data is not None and output_folder:
        output_path = os.path.join(os.getcwd(), output_folder)
        os.makedirs(output_path, exist_ok=True)

        st.write("Extracting account numbers...")

        # Saving the uploaded files
        file_path = os.path.join(output_path, "temp_file.pdf")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        data = io.BytesIO(uploaded_data.getvalue())
        df = pd.read_excel(data)  # Assuming uploaded file is in Excel format

        extracted_numbers = extract_account_numbers(file_path, output_path, df)

        # Creating a ZIP file containing all extracted PDFs
        zip_file_path = os.path.join(output_path, "extracted_pdfs.zip")
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in extracted_numbers:
                zipf.write(file, os.path.basename(file))

        st.success(f"All PDFs extracted! Download the ZIP file containing all files.")
        st.download_button(label="Download All Extracted PDFs", data=open(zip_file_path, "rb").read(), file_name="extracted_pdfs.zip")


if __name__ == "__main__":
    main()
