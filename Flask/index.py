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
OPENAI_API_KEY ="Your_api_key"
openai.api_key = OPENAI_API_KEY


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
    return summary


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/',methods=['POST'])
def predict():
    # print("HI")
    event=json.loads(request.data)
    spe = event["speech"]
    # print(type(spe))
    response = summ_batches(spe)
    # print(response)
    return jsonify(response)

if __name__=='__main__':
    app.run(debug=True) 
