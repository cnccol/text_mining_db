import re
import hashlib
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

UPDATE_SQL = "UPDATE docs_leidos SET leido = %s WHERE path_to_file = %s"
SELECT_QUERY = "SELECT path_to_file FROM docs_leidos where leido = %s and grupo = %s"



# Functions to check validity of a file

def bad_file(path_file):
    os.stat(path_file).st_size == 0 or path_file.startswith("~") or path_file.startswith(".")

def check_file(path_file):
    return not(path_file in UNREAD_FILE or bad_file(path_file))

# Functions to process doc and docx path_files
def doc2docx(path_file):
    subprocess.call(["soffice", "--headless", "--convert-to", "docx", path_file])

def read_docx(path_file):
    text = docx2txt.process(path_file)
    text = text.replace("-\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text, 1

def clean_text(text):
    text = text.replace("-\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def process_doc(path_file):
    doc2docx(path_file)
    try:
        return read_docx(path_file+"x")
    except FileNotFoundError:
        return None, 0

def process_docx(path_file):
    try:
        return read_docx(path_file)
    except BadZipFile:
        return  None, 0

# Functions to process pdf path_files
def read_pdf_as_text_to_list(path_file):
    with open(path_file, 'rb') as f:
        pdfdoc = PyPDF2.PdfFileReader(f)

        n_pages = pdfdoc.numPages

        count = 0
        text_list = []

        while count < n_pages:
            pageobj = pdfdoc.getPage(count)
            try:
                text_list.append(pageobj.extractText())
                #fprint(text_list)
            except (KeyError, AttributeError, zlib.error, InvalidOperation):
                print('non content in page')
                text_list.append(" ")
            count += 1
    #print("llego aca")
    return text_list

def read_pdf_as_image_to_list(path_file, dpi):
    # print("images")
    text_list = []
    n_page = _page_count(path_file)

    for i in range(1, n_page+1):
        # print(i,text_list)
        try:
            pages = pdf2image.convert_from_path(path_file, dpi, first_page = i, last_page = i)
            for page in pages:
                text = str(pytesseract.image_to_string(page, lang="spa"))
                text_list.append(text)
        except Image.DecompressionBombError:
            print('image size error')
            text_list.append('')
        pass
    #print(text_list)
    return text_list

def process_pdf(path_file):
    # print("ENTRO")
    if path_file in MANDATORY_READ_AS_IMAGE:
        text_list =  read_pdf_as_image_to_list(path_file, 450)
        whole_text = ' '.join(text_list)
        return clean_text(whole_text), 1
    else:
        try:
            text_list = read_pdf_as_text_to_list(path_file)
            whole_text = ' '.join(text_list)
            whole_text = clean_text(whole_text)
            # print(whole_text)
        except (OSError, ValueError, PyPDF2.utils.PdfReadError):
            print('File has not been decrypted. Reading as image...')
            try:
                text_list = read_pdf_as_image_to_list(path_file, 450)
                return clean_text(' '.join(text_list)), 1
            except pdf2image.exceptions.PDFPageCountError:
                return ' ', 0
                pass
            pass

        if (len(whole_text) < 100) or not (
            (whole_text.lower().find(' de ') >= 0) or
            (whole_text.lower().find(' con ') >= 0)):
            # print("leyo texto no encontro")
            try:
                text_list = read_pdf_as_image_to_list(path_file, 450)
                return clean_text(' '.join(text_list)), 1
            except pdf2image.exceptions.PDFPageCountError: #Unable to get page count / password required.
                return '',0
            pass
        else:
            return whole_text,1

def process_document(path_file):
    if not check_file(path_file):
        print("FAIL", path_file)
        return "", 0
    if path_file.lower().endswith('.pdf'):
        return process_pdf(path_file)
    if path_file.lower().endswith('.doc'):
        return process_doc(path_file)
    if path_file.lower().endswith('.docx'):
        return process_docx(path_file)

def process_all_docs(typ,where):
   mydb = connector.connect(
  host="host",
  user="user",
  passwd="pass",
  database="db"
)

    cursor = mydb.cursor()
    cursor.execute(SELECT_QUERY,(0,typ))
    list_data =  [x[0] for x in cursor.fetchall()]

    len_of_data = len(list_data)
    print(len_of_data)
    for i,document in enumerate(list_data):
        # print(document)
        # print("-----------------------------------")
        text, proccesed = process_document(document)
        if proccesed == 1:
            cursor.execute(UPDATE_SQL,(1,document))
            result = {"file": document, "text": text}
            # print(result)
            with open("/home/{}/pickles/{}/{}.pickle".format(where,typ,hashlib.md5(document.encode()).hexdigest()), "wb") as f:
                pickle.dump(result,f)
            if (i%10) == 0:
                mydb.commit()

        print("goes {}%".format(i*1.0/len_of_data*1.0))
    mydb.commit()
