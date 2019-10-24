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


NEW_PICKLE = 'tripla_Relec_li109.pickle'
ORIG_PICKLE = 'tripla_Orig_li109.pickle'


# Definition
##############
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



# Open old tripla
##################
try:
    with open(ORIG_PICKLE, 'rb') as f:
        orig_read_file, orig_read_text, orig_read_type = pickle.load(f)
except:
    orig_read_file, orig_read_text, orig_read_type = [], [], []
    print('tripla orig no abrio')

try:
    with open(NEW_PICKLE, 'rb') as f:
        new_read_file, new_read_text, new_read_type = pickle.load(f)
except:
    new_read_file, new_read_text, new_read_type = [], [], []
    print('tripla new no abrio')

orig_dict = {filename: (text, read_type) for filename, text, read_type
             in zip(orig_read_file, orig_read_text, orig_read_type)}
new_dict = {filename: (text, read_type) for filename, text, read_type
            in zip(new_read_file, new_read_text, new_read_type)}

directory = os.getcwd()
# directory =  '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/2019'
## Number of pdfs in folders
n_pdfs = 0
n_docs = 0
for root, dirs, files in os.walk(directory):
    for file_name in files:
        if file_name.endswith('.pdf'):
            n_pdfs += 1

        if file_name.endswith(".docx") or file_name.endswith(".doc"):
            if file_name.startswith("~"):
                continue
            elif file_name.startswith("."):
                continue
            else:
                n_docs += 1        

n_files = n_pdfs + n_docs 
print('Número de pdfs y docs en ruta:', str(n_files))
print('Tamaño tripla original:', len(orig_read_file), len(orig_read_text), len(orig_read_type))
print('Tamaño tripla lectura:', len(new_read_file), len(new_read_text), len(new_read_type))
t0total  = time.time()



# Read pdfs doc/docx files
###########################
unread_file = ['/mnt/60B24185B24160A0/text_mining/Licitaciones/2018/06 JUnio/BANCO DE LA REPÚBLICA ENCUESTA COMERCIANTES GANADA/Propuesta Centro Nacional de Consultoría S.A.pdf',
               '/mnt/60B24185B24160A0/text_mining/Licitaciones/2019/07 JULIO 19/FINDETER/Sobre No. 1.pdf',
               '/mnt/60B24185B24160A0/text_mining/Licitaciones/2019/07 JULIO 19/FINDETER/Sobre No. 2.pdf',
               '/mnt/60B24185B24160A0/text_mining/Licitaciones/2019/07 JULIO 19/FINDETER/Documentos Entidad/Acta de Cierre (1).pdf']

mandatory_read_as_image = ['/mnt/60B24185B24160A0/text_mining/Licitaciones/2018/11 Noviembre/DNP 40.000 EMPLEOS 008 - ECONOMETRIA SEI/PROPUESTAS OPONENTES/CM CONSULTORES/Experiencia Adicional c-1-100 Parte 1.pdf',
                           '/mnt/60B24185B24160A0/text_mining/Licitaciones/2018/11 Noviembre/DNP 40.000 EMPLEOS 008 - ECONOMETRIA SEI/PROPUESTAS OPONENTES/CM CONSULTORES/Experiencia Adicional c-101-200 Parte 2.pdf',
                           '/mnt/60B24185B24160A0/text_mining/Licitaciones/2018/11 Noviembre/DNP 40.000 EMPLEOS 008 - ECONOMETRIA SEI/PROPUESTAS OPONENTES/Experiencia Adicional c-201-300 Parte 3.pdf',
                           '/mnt/60B24185B24160A0/text_mining/Licitaciones/2018/11 Noviembre/DNP 40.000 EMPLEOS 008 - ECONOMETRIA SEI/PROPUESTAS OPONENTES/Experiencia Adicional Directora- Anexo 6 y 7.pdf',]

whole_texts_list = []
lists_tuple = ([], [], []) # (lista_nombres, ista_textos, lista_tipos)

try:
    ii=1
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            t0 = time.time()
            file_path = os.path.join(root, file_name)
            file_info = os.stat(file_path)              ##########
            # pdfs
            if file_name.endswith('.pdf') and os.stat(file_path).st_size != 0:
                if file_path in new_dict:
                    t1 = time.time()
                    print('NEW ALREADY READ '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))            


                elif file_path in orig_dict:
                    whole_text = orig_dict[file_path][0]
                    read_type = orig_dict[file_path][1]
                    
                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    # with open(NEW_PICKLE, 'wb') as f:
                    #     pickle.dump(lists_tuple, f)
 
                    t1 = time.time()
                    print('ORIGINAL ALREADY READ '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))


                elif file_path in unread_file:
                    whole_text = ''
                    read_type = 'it_can_not_be_read'
                    
                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    with open(NEW_PICKLE, 'wb') as f:
                        pickle.dump(lists_tuple, f)

                    t1 = time.time()
                    print('it_can_not_be_read '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))


                elif file_path in mandatory_read_as_image:
                    t1 = time.time()
                    print('Reading as image:', file_path)

                    text_list = read_pdf_as_image_to_list(file_path, 450, 1)
                    whole_text = ' '.join(text_list)
                    read_type = 'image_pdf'
                    t1 = time.time()
                    print('READ AS IMAGE '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))

                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    with open(NEW_PICKLE, 'wb') as f:
                        pickle.dump(lists_tuple, f)
               
                    
                else:

                    print('Reading as text:', file_path)

                    try:    
                        text_list = read_pdf_as_text_to_list(file_path)
                        t1 = time.time()
                        print('READ AS TEXT '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                        whole_text = ' '.join(text_list)
                        read_type = 'text_pdf'
                    except (OSError, ValueError, PyPDF2.utils.PdfReadError):
                        print('File has not been decrypted. Reading as image...')
                        try: 
                            text_list = read_pdf_as_image_to_list(file_path, 450, 1)
                            t1 = time.time()
                            print('READ AS IMAGE '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = ' '.join(text_list)
                            read_type = 'image_pdf'
                        except pdf2image.exceptions.PDFPageCountError: #Unable to get page count / password required.
                            t1 = time.time()
                            print('it_can_not_be_read: Unable to get page count / password required. '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = ' '
                            read_type = 'it_can_not_be_read'
                            pass
                        pass

                    if (len(whole_text) < 100) or not (
                            (whole_text.lower().find(' de ') >= 0) or 
                            (whole_text.lower().find(' con ') >= 0)):
                        print('Reading as image...')
                        try:
                            text_list = read_pdf_as_image_to_list(file_path, 450, 1)
                            t1 = time.time()
                            print('READ AS IMAGE '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = ' '.join(text_list)
                            read_type = 'image_pdf'
                        except pdf2image.exceptions.PDFPageCountError: #Unable to get page count / password required.
                            t1 = time.time()
                            print('it_can_not_be_read: Unable to get page count / password required. '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = ''
                            read_type = 'it_can_not_be_read'
                            pass

                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    with open(NEW_PICKLE, 'wb') as f:
                        pickle.dump(lists_tuple, f)

                ii+=1


            # doc/dox
            if file_name.endswith((".docx", ".doc")) and os.stat(file_path).st_size != 0:
                if file_path in new_dict:
                    t1 = time.time()
                    print('NEW ALREADY READ '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))            

                elif file_path in orig_dict:
                    whole_text = orig_dict[file_path][0]
                    read_type = orig_dict[file_path][1]
                    
                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    # with open(NEW_PICKLE, 'wb') as f:
                    #     pickle.dump(lists_tuple, f)

                    t1 = time.time()
                    print('ORIGINAL ALREADY READ '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))


                elif file_path in unread_file:
                    whole_text = ''
                    read_type = 'it_can_not_be_read'
                    
                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    with open(NEW_PICKLE, 'wb') as f:
                        pickle.dump(lists_tuple, f)

                    t1 = time.time()
                    print('it_can_not_be_read '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))


                elif file_name.endswith((".docx", ".doc")) & file_name.startswith("~"):
                    print("Bad file ")
                    continue
                    
                elif file_name.endswith((".docx", ".doc")) & file_name.startswith("."):
                    print("Hidden file ")
                    continue               
                    
                else:
                    
                    print('Reading as doc:', file_path)

                    if file_name.endswith(".docx"):
                        #nombre = file_path
                        try:
                            whole_text = leer_docx(file_path)
                            read_type = "docx"
                            t1 = time.time()
                            print("READ AS DOCX: " +str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                        except BadZipFile: # File is not a zip file (password required)
                            t1 = time.time()
                            print('it_can_not_be_read: File is not a zip file (password required). '+str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = ''
                            read_type = 'it_can_not_be_read'
                            pass

                    elif file_name.endswith(".doc"):
                        #nombre = file_path
                        doc_2_docx(file_path)
                        temp_docx_path = os.getcwd() + "/" + file_name + "x"
                        try:
                            whole_text = leer_docx(temp_docx_path)
                            t1 = time.time()
                            print("DOC TRANSFORMED AND READ: " +str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            read_type = "doc"
                            os.remove(temp_docx_path)
                        except FileNotFoundError:
                            t1 = time.time()
                            print("Could not open file. " +str(ii),str(round(ii / n_files * 100, 2)),round(t1-t0, 2))
                            whole_text = "" 
                            read_type = 'it_can_not_be_read'
                            pass


                    new_read_file.append(file_path)
                    new_read_text.append(whole_text)
                    new_read_type.append(read_type)

                    lists_tuple = (new_read_file, new_read_text, new_read_type)
                
                    with open(NEW_PICKLE, 'wb') as f:
                        pickle.dump(lists_tuple, f)

                ii+=1
            # print(round(t1-t0, 2))


except KeyboardInterrupt:

    lists_tuple = (new_read_file, new_read_text, new_read_type)
        
    with open(NEW_PICKLE, 'wb') as f:
        pickle.dump(lists_tuple, f)

    pass


print('Número de pdfs y docs en ruta:', str(n_files))
print('Tamaño tripla original:', len(orig_read_file), len(orig_read_text), len(orig_read_type))
print('Tamaño tripla lectura:', len(new_read_file), len(new_read_text), len(new_read_type))
t1total = time.time()
print('Tiempo total lectura:', round(t1total-t0total, 2))
