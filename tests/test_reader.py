import unittest
from text_mining.reader import Reader

class TestReader(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()
        
    def test_clean_text(self):
        self.assertEqual("menos mal que no hay un bug grave", self.reader.clean_text("menos   mal que \n no hay un \t   -\n bug grave"))

    def test_read_docx_work(self):
        self.assertEqual(("menos mal que no hay un bug grave",1), self.reader.read_docx("tests/files/test.docx"))

    def test_read_docx_error(self):
        self.assertEqual((None, 0),self.reader.read_docx("tests/files/test_bad.docx"))