from django.shortcuts import render,HttpResponse,redirect
from .models import myuploadfile
import cv2
import numpy as np
import pytesseract
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
def index(request):
    return render(request,"index.html")

def index1(request):
    context = {
        "data":myuploadfile.objects.all(),
    }
    return render(request,"index1.html",context)

global s_vectors

def text_plagiarism():
    path = "C:\myproj\myfileapp"
    os.chdir(path)
    pdftotext()
    imgtotext()
    student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
    student_notes = [open(File).read() for File in student_files]


    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))
    plagiarism_results = set()

    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            sim_score_per = sim_score*100
            sim_score_dec = "{:.2f}".format(sim_score_per) + "%"
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score_dec)
            plagiarism_results.add(score)
    
    for i in student_files:
        os.remove(i)
    return plagiarism_results
    


def pdftotext():
    doc_name = [doc for doc in os.listdir() if doc.endswith('.pdf')]

    for name in doc_name:
        pdfFileObj = open(name,'rb')
        pdfreader = PyPDF2.PdfFileReader(pdfFileObj)
        no_of_pages = pdfreader.numPages
                
                
        name1 = name.split('.')
        res1=name1[0]
        res1 = res1 + ".txt"
        f = open(res1,"w+")
        string = ""
        for i in range(0,no_of_pages):
            pageObj = pdfreader.getPage(i)
            string = string + pageObj.extractText()
            #print(pageObj.extractText())
            f.write(string)   
        pdfFileObj.close()
        os.remove(name) 
       
        
def imgtotext():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img_name = [doc for doc in os.listdir() if doc.endswith('.png')]

    for name in img_name:
        img = cv2.imread(name)
        imp = cv2.resize(img, None, fx=0.5, fy=0.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)

        config = "--psm 4"
        text = pytesseract.image_to_string(adaptive_threshold, config=config)

        name1 = name.split('.')
        res1=name1[0]
        res1 = res1 + ".txt"
        f = open(res1,"w+")

        outfile = open(res1, 'a+',encoding='utf-8')
        outfile.write(text)
        outfile.close()
        newfile = open(res1, 'r',encoding='utf-8')
        os.remove(name)        


def send_files(request):
    if request.method == "POST" :
        name = request.POST.get("filename")
        myfile = request.FILES.getlist("uploadfoles")
        
        for f in myfile:
            myuploadfile(f_name=name,myfiles=f).save()
        


        all_mix = list(text_plagiarism())
        percents=[]
        docs, doc = [],[]
        for n in range(len(all_mix)):
            percents.append(all_mix[n][2])
            doc.append(all_mix[n][:2])
        
        for elements in doc:
            str = ' & '.join(elements)
            docs.append(str)
        
        context1={
            "data1" : docs,
            "data2" : percents,
            
        }
              
        return render(request,"final.html",context1)
        



        
