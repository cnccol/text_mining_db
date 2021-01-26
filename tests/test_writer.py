import unittest
from os import path
from text_mining.writer import Writer
from text_mining.database import db
from text_mining.models import Document


class TestReader(unittest.TestCase):
    def setUp(self):
        self.writer = Writer()

    def test_writer(self):
        data = {'id':'test','path':'test','content':'test','readed':True}
        self.assertEqual(True,
                self.writer.save(Document(**data), 'test'))
        doc = db.collection('test').document(str(data['id'])).get()
        self.assertEqual(data, doc.to_dict())
