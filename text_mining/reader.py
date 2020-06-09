import docx2txt
import os
from zipfile import BadZipFile
import subprocess


class Reader:
    """Class that implements methods to read files in different formats"""

    def clean_text(self, text):

        """Helper method to clean text e.g. remove extra spaces, tabs and line changes

        Args:
            text (str): The text to clean

        Returns:
            text: text without extra spaces, tabs and line changes
        """

        text = text.replace("-\n", " ")
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
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
            return self.clean_text(docx2txt.process(path_to_docx)), 1
        except BadZipFile:
            return None, 0

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

        """Method to delete extra .docx files

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
            return None, 0
