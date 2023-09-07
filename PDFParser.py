import PyPDF2

# This file converts pdf to plain text.
from pypdf import PdfReader


def main():
    reader = PdfReader("data/paper3.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(len(text.split(' ')))
    print(text)


if __name__ == '__main__':
    main()
