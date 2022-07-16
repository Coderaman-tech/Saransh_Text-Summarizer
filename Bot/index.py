import openai
import wget
import pathlib
import pdfplumber
import numpy as np
from flask import Flask,request,Response
import requests
import json
import nltk
from flask_sslify import SSLify
import os
nltk.download('punkt')

tldr_tag = "\n tl;dr:"
SUMMARIZE_PREFIX = "Summarize this for a second-grade student:\n\n"
ENGINE = "text-curie-001"
BATCH_SIZE = 500
NUM_TOKENS = 125
OPENAI_API_KEY = 
Teletoken = 
openai.api_key = OPENAI_API_KEY

welcome = "Hi, I am Saransh , a Text-Summarizer Bot. Sometime you have long Paragraph or Pages and you are don't want to read it. So, Use Me. You can send text messages or pdf and I can share Summary of it"

def getPaper(paper_url, filename="random_paper.pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local path to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)    
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath

def post_processing(response_text):
    try:
        fullstop_index = response_text.rindex('.')
        response_text = response_text[:fullstop_index + 1]
    except Exception as e:
        print(e)
    return response_text.replace('\\n', '')

def showPaperSummary(input_text):
    gpt3_prompt = SUMMARIZE_PREFIX + input_text + tldr_tag
    response = openai.Completion.create(
        engine=ENGINE,
        prompt=gpt3_prompt,
        temperature=0,
        max_tokens=NUM_TOKENS,
        top_p=1.0,
        frequency_penalty=1.0,
        presence_penalty=1.0
    )
    batch_summary = response["choices"][0]["text"]

    return post_processing(response_text = batch_summary)    

def summ_batches(input_text, chat_id):
    if input_text == "/start":
      summary = welcome
    else:   
      sentences = nltk.tokenize.sent_tokenize(input_text)
      tokens = 0
      batch_sentence = ""
      batches = []
      for sentence in sentences:
        tokens = tokens + len(nltk.word_tokenize(sentence))
        if tokens <= BATCH_SIZE:
            batch_sentence = batch_sentence + sentence
        else:
            batches.append(batch_sentence)
            batch_sentence = sentence
            tokens = len(nltk.word_tokenize(sentence))
      if batch_sentence not in batches:
        batches.append(batch_sentence) 
      summary = ''
      for batch in batches:
        response = showPaperSummary(batch)
        summary = summary + response
    requests.get("https://api.telegram.org/bot"+Teletoken+"/sendMessage?chat_id="+chat_id+"&text="+summary)    
    pass

from flask import Flask, request

app = Flask(__name__)
sslify = SSLify(app)
@app.route('/hi')
def index():
    return "<h1>Hello</h1>"

@app.route('/', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        msg = request.json
        content = msg["message"]
        chat_id = str(content["chat"]["id"])
        # text = content["text"]
        # summ_batches(text,chat_id)

        if "text" in content:
             text = content["text"]
             
        elif "document" in content:
             file_id = content["document"]["file_id"]  
             docreq = requests.get("https://api.telegram.org/bot"+Teletoken+"/getFile?file_id="+file_id)
             file_path = json.loads(docreq.content)["result"]["file_path"]
             print(file_path)
             getPaper("https://api.telegram.org/file/bot"+Teletoken+"/"+file_path,filename="random_paper.pdf"+str(0))
             paperFilePath = "random_paper.pdf"+str(0)
             paperContent = pdfplumber.open(paperFilePath).pages
             text = ""
             for page in paperContent:    
                text = text + " " +page.extract_text()   
             os.remove("random_paper.pdf0")        
    print("HI")
    summ_batches(text,chat_id)
    return Response("ok", status=200)


        
