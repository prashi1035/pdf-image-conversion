# This project is written in python 3.6 
#The purpose of this project is to convert the list of pdfs in a directory to images
#output images will be saved in images folder

#importing the required libraries
import os
import sys
import io
import time

import pandas as pd
import PyPDF2
from PyPDF2 import PdfFileReader
from wand import image 
from wand.image import Image
from wand.color import Color

def pdf_page_to_png(src_pdf, pagenum = 0, resolution = 100,):
    ''' convert the each page in pdf to image'''
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf1 = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))
    dst_pdf1.addPage(src_pdf.getPage(pagenum))
    pdf_bytes = io.BytesIO()
    dst_pdf1.write(pdf_bytes)
    pdf_bytes.seek(0)
    img =image.Image(file = pdf_bytes, resolution = resolution)
    img.background_color = Color('white')
    img.alpha_channel = 'remove'
    img.convert("jpg")

    return img


def pdftoimage_conversion(pdfs_path,resol):
    ''' Takes input pdfs path and convert the pdf to images and save in the directiory images'''
    try:
        dir_path = os.path.join(pdfs_path,'images')
        if not (os.path.exists(dir_path)):
            os.makedirs(dir_path)
        start_time = time.time()
        files = [f for f in os.listdir( pdfs_path) if f.lower().endswith((".pdf"))]
        for f in files:
            pdf=PdfFileReader(open(os.path.join( pdfs_path, f),'rb'))
            for i in range(pdf.getNumPages()):
                file_name ="{0}_{1}.jpg".format(f[:-4],i)
                dir_path_file = os.path.join(dir_path,file_name)
                if not os.path.isfile(dir_path_file):
                    img = pdf_page_to_png(pdf, pagenum = i, resolution = resol)
                    img.save(filename = (os.path.join(dir_path, file_name)))
        end_time = time.time()
        print("Done!!!!")
        print ("Time taken to convert the pdfs to images  {0} seconds".format(end_time - start_time))
        response = "Conversion of pdfs to images is done"
    except Exception as ex:
        response = ex
    finally:
        print (response)
        return response
    
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Usage: python pdf2imgcon.py path to pdf files resolution_between 100 to 500\nexample python pdf2imgcon.py path/pdfs 100')
        sys.exit(1)
    pdfs_path = sys.argv[1]
    resol = int(sys.argv[2])
    res_check = False
    while not res_check:
        if resol >= 100 and resol<= 500:
            res_check = True
            pdftoimage_conversion(pdfs_path,resol)
        else:
            print("please enter the resolution between 100 and 500\n")
            resol = int(input("Enter the resolution for the images between 100 and 500 :: "))
    