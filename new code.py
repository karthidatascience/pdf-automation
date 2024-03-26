
import streamlit as st
from PyPDF2 import PdfWriter, PdfReader
import os
import pandas as pd
import io
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
        extracted_numbers.append(acc_num)
    return extracted_numbers
def main():
    st.title("PDF Account Number Extraction")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    uploaded_data = st.file_uploader("Upload a Pandas file", type=["csv", "xlsx"])
    if uploaded_file is not None and uploaded_data is not None:
        output_folder = r'Hotel Extraction Path'  # Specify your desired output folder here
        os.makedirs(output_folder, exist_ok=True)
        st.write("Extracting account numbers...")
        # Saving the uploaded files
        file_path = os.path.join(output_folder, "temp_file.pdf")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        data = io.BytesIO(uploaded_data.getvalue())
        df = pd.read_excel(data)  # Assuming uploaded file is in Excel format
        extracted_numbers = extract_account_numbers(file_path, output_folder, df)
        st.write(f"Extracted Account Numbers:")
        for number in extracted_numbers:
            st.write(number)
if __name__ == "__main__":
    main()
