import re
import os
import pickle
import numpy as np
import pandas as pd
import PyPDF2
from PIL import Image
import pytesseract
import sys
import pdf2image
from pdf2image.pdf2image import _page_count
import time
import zlib
from decimal import InvalidOperation
# Read doc docx
import subprocess
import pdb
import sys
import docx2txt
import time
from zipfile import BadZipFile

import mysql.connector as connector 

SELECT_QUERY  = "SELECT path_to_file FROM docs_leidos where leido =  0"

def read_pdf_as_text_to_list(file_path):
    with open(file_path, 'rb') as f:
        pdfdoc = PyPDF2.PdfFileReader(f)

        n_pages = pdfdoc.numPages

        count = 0
        text_list = []
        # Read by pages
        while count < n_pages:
            pageobj = pdfdoc.getPage(count)
            try:
                text_list.append(pageobj.extractText())
            except (KeyError, AttributeError, zlib.error, InvalidOperation): # non content in page / class decimal.ConversionSyntax
                print('non content in page')
                text_list.append(" ")
            count += 1

    return text_list


def read_pdf_as_image_to_list(file_path, dpi, batch_n_pages):
    text_list = []
    n_pages = _page_count(file_path)

    n_batches = int((n_pages-1) / batch_n_pages // 1)

    for i in range(n_batches):
        try:
            pages = pdf2image.convert_from_path(
                file_path, dpi, first_page=int(i*batch_n_pages + 1),
                last_page=int(i*batch_n_pages + batch_n_pages))
            for page in pages:
                text = str(((pytesseract.image_to_string(page, lang="spa"))))
                # tex = tex.replace("-\n", " ")
                text_list.append(text)
        except Image.DecompressionBombError: #Image size exceeds limit of 178956970 pixels.
            print('image size error in page')
            text_list.append('')
            pass

    try:
        pages = pdf2image.convert_from_path(
            file_path, dpi, first_page=n_batches*batch_n_pages + 1, last_page=n_pages)

        for page in pages:
            text = str(((pytesseract.image_to_string(page, lang="spa"))))
            # tex = tex.replace("-\n", " ")
            text_list.append(text)
    except Image.DecompressionBombError: #Image size exceeds limit of 178956970 pixels.
        print('image size error in page')
        text_list.append('')
        pass

    return text_list


def doc_2_docx(path):
    subprocess.call(["soffice", "--headless", "--convert-to", "docx", path])


def leer_docx(path):
    text = docx2txt.process(path)
    text = text.replace("-\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    for ii in range(2,50):
        text = text.replace((" "*ii), " ")
    text = text.replace("  ", " ")
    return text

def process_document(document_path):
