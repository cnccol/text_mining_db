import docx2txt
from zipfile import BadZipFile

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
            return  None, 0