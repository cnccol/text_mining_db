import docx2txt
import os
from zipfile import BadZipFile
import subprocess
import textract
import string
import pytesseract
import pdf2image
from pdf2image.pdf2image import pdfinfo_from_path
from PIL import Image


class Reader:
    """Class that implements methods to read files in different formats"""

    def clean_text(self, text):
        """Method to clean text e.g. remove extra spaces, tabs and line changes

        Args:
            text (str): The text to clean

        Returns:
            text: text without extra spaces, tabs and line changes
        """
        text = text.translate(str.maketrans(string.whitespace,  ' '*len(string.whitespace))).strip()
        while '  ' in text:
            text = text.replace('  ', ' ')
        return text

    def read_docx(self, path_to_docx):
        """Method to read .docx files returns text in the file and a flag to show completion

        Args:
            path_to_docx (str): path to the docx file to read

        Return:
            text: text readed from the file.
            flag: bool value that shows that the reading was succesful
        """
        try:
            return self.clean_text(docx2txt.process(path_to_docx)), True
        except BadZipFile:
            return None, False

    def doc2docx(self, path_to_doc):
        """Method to convert .doc files into docx files

        Args:
            path_to_doc (str): path to the doc file to read

        Return:
            path_to_docx (str): path to the new docx file
        """
        if(os.path.exists(path_to_doc)):
            subprocess.call(["soffice", "--headless", "--convert-to", "docx", path_to_doc],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return (path_to_doc+"x").split("/")[-1]

    def delete_docx(self, path_to_docx):
        """Method to delete extra .docx filesflag: bool value that shows that the reading was succesful

        Args:
            path_to_docx (str): path to the docx file to delete

        """
        if(os.path.exists(path_to_docx)):
            os.remove(path_to_docx)

    def read_doc(self, path_to_doc):
        """Method to read .doc files returns text in the file and a flag to show completion

        Args:
            path_to_doc (str): path to the doc file to read

        Return:
            text: text readed from the file.
            flag: bool value that shows that the reading was succesful
        """
        path_to_docx = self.doc2docx(path_to_doc)
        try:
            text, flag = self.read_docx(path_to_docx)
            self.delete_docx(path_to_docx)
            return text, flag
        except FileNotFoundError:
            return None, False

    def read_pdf_txt(self, path_to_pdf):
        """Method to read .pdf files as text files returns text in the file

        Args:
            path_to_pdf (str): path to the pdf file

        Return:
            text: text readed from the file.
        """
        try:
            return self.clean_text(textract.process(path_to_pdf).decode('utf8'))
        except textract.exceptions.MissingFileError:
            return None

    def read_pdf_image(self, path_to_pdf, dpi=450):
        """Method to read .pdf files as images files returns text in the file

        Args:
            path_to_pdf (str): path to the pdf file

        Return:flag: bool value that shows that the reading was succesful
            text: text readed from the file.
        """
        text_list = []
        try:
            n_pages = pdfinfo_from_path(path_to_pdf)["Pages"]

            for i in range(1, n_pages+1):
                try:
                    pages = pdf2image.convert_from_path(path_to_pdf, dpi, first_page=i, last_page=i)
                    for page in pages:
                        text = str(pytesseract.image_to_string(page, lang="spa"))
                        text_list.append(text)
                except Image.DecompressionBombError:
                    text_list.append('')
            return self.clean_text(' '.join(text_list))
        except pdf2image.exceptions.PDFPageCountError:
            return None

    def valid_text(text):
        """Method to verify the validity of a text.

        Args:
            text (str): text to check

        Return:
            valid: flag that shows if the text is vaild.
        """
        if text is None:
            return False
        if len(text) < 100:
            return False
        if text.lower().find(' de ')==0 or text.lower().find(' con '):
            return False
        return True

    def read_pdf(self, path_to_pdf):
        """Method to read .pdf files

        Args:
            path_to_pdf (str): path to the pdf file

        Return:
            text: text readed from the file.
            flag: bool value that shows that the reading was succesful
        """
        text = self.read_pdf_txt(path_to_pdf)
        if not valid_text(text):
            text = self.read_pdf_image(path_to_pdf)
        return text, valid_text(text)
