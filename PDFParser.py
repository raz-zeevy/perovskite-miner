# This file converts pdf to plain text.
from pypdf import PdfReader

def get_txt_from_pdf(pdf_path : str) -> str:
    """
    extracts txt content out of pdf
    :param pdf_path: the path of the pdf
    :return:
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    # print(len(text.split(' ')))
    # print(text)
    return text

if __name__ == '__main__':
    get_txt_from_pdf()
