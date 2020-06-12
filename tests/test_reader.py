import unittest
from os import path
from text_mining.reader import Reader


class TestReader(unittest.TestCase):
    def setUp(self):
        self.reader = Reader()

    def test_clean_text(self):
        self.assertEqual("menos mal que no hay un bug grave",
                         self.reader.clean_text("menos   mal que \n no hay un \t  \n bug grave"))

    def test_read_docx_work(self):
        self.assertEqual(("menos mal que no hay un bug grave", 1), self.reader.read_docx("tests/files/test.docx"))

    def test_read_docx_error(self):
        self.assertEqual((None, 0), self.reader.read_docx("tests/files/test_bad.docx"))

    def test_doc2docx_and_remove(self):
        path_to_docx = self.reader.doc2docx("tests/files/testDoc.doc")
        self.assertTrue(path.exists(path_to_docx))
        self.reader.delete_docx(path_to_docx)
        self.assertFalse(path.exists(path_to_docx))

    def test_doc2docx_and_remove_noexist(self):
        path_to_docx = self.reader.doc2docx("tests/files/testDoc2.doc")
        self.assertFalse(path.exists(path_to_docx))
        self.reader.delete_docx(path_to_docx)
        self.assertFalse(path.exists(path_to_docx))

    def test_read_doc(self):
        path_to_doc = "tests/files/testDoc.doc"
        self.assertEqual(("Texto de prueba", 1), self.reader.read_doc(path_to_doc))

    def test_read_doc_error(self):
        path_to_doc = "tests/files/testDoc2.doc"
        self.assertEqual((None, 0), self.reader.read_doc(path_to_doc))

    def test_read_pdf_as_txt(self):
        path_pdf = "tests/files/test.pdf"
        self.assertEqual("menos mal que no hay un bug grave", self.reader.read_pdf_txt(path_pdf))

    def test_read_pdf_as_txt_error(self):
        path_pdf = "tests/files/test2.pdf"
        self.assertEqual(None, self.reader.read_pdf_txt(path_pdf))
