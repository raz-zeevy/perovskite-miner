from PDFParser import get_txt_from_pdf

if __name__ == '__main__':
    pdf_path = r"data/paper1.pdf"
    data_path = r"data/db_output1.pdf"
    print(get_txt_from_pdf(pdf_path))
