from regex import W
import wget
import pathlib
import pdfplumber
import numpy as np
from flask import Flask,request
import requests
import time
import urllib.request
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import re
import string
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize as nlkt_sent_tokenize
from nltk.tokenize import word_tokenize as nlkt_word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
import numpy as np
from scipy.spatial.distance import cosine
from flask import Flask, jsonify,request
import json
import os

n=0
bot_token = 
welcome = "Hi, I am Saransh , a Text-Summarizer Bot. Sometime you have long Paragraph or Pages and you are don't want to read it. So, Use Me. You can send text messages or pdf and I can share Summary of it"

def getPaper(paper_url, filename="random_paper.pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local path to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)    
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath

def similarity(v1, v2):
    score = 0.0
    if np.count_nonzero(v1) != 0 and np.count_nonzero(v2) != 0:
        score = ((1 - cosine(v1, v2)) + 1) / 2
    return score

def sent_tokenize(text):
    sents = nlkt_sent_tokenize(text)
    sents_filtered = []
    for s in sents:
        sents_filtered.append(s)
    return sents_filtered

def cleanup_sentences(text):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(text)
    sentences_cleaned = []
    for sent in sentences:
        words = nlkt_word_tokenize(sent)
        words = [w for w in words if w not in string.punctuation]
        words = [w for w in words if not w.lower() in stop_words]
        words = [w.lower() for w in words]
        sentences_cleaned.append(" ".join(words))
    return sentences_cleaned

def get_tf_idf(sentences):
    vectorizer = CountVectorizer()
    sent_word_matrix = vectorizer.fit_transform(sentences)

    transformer = TfidfTransformer(norm=None, sublinear_tf=False, smooth_idf=False)
    tfidf = transformer.fit_transform(sent_word_matrix)
    tfidf = tfidf.toarray()

    centroid_vector = tfidf.sum(0)
    centroid_vector = np.divide(centroid_vector, centroid_vector.max())

    feature_names = vectorizer.get_feature_names()

    relevant_vector_indices = np.where(centroid_vector > 0.3)[0]

    word_list = list(np.array(feature_names)[relevant_vector_indices])
    return word_list

#Populate word vector with all embeddings.
#This word vector is a look up table that is used
#for getting the centroid and sentences embedding representation.
def word_vectors_cache(sentences, embedding_model):
    word_vectors = dict()
    for sent in sentences:
        words = nlkt_word_tokenize(sent)
        for w in words:
            word_vectors.update({w: embedding_model.wv[w]})
    return word_vectors

# Sentence embedding representation with sum of word vectors
def build_embedding_representation(words, word_vectors, embedding_model):
    embedding_representation = np.zeros(embedding_model.vector_size, dtype="float32")
    word_vectors_keys = set(word_vectors.keys())
    count = 0
    for w in words:
        if w in word_vectors_keys:
            embedding_representation = embedding_representation + word_vectors[w]
            count += 1
    if count != 0:
        embedding_representation = np.divide(embedding_representation, count)
    return embedding_representation

def summarize(text, emdedding_model):
    raw_sentences = sent_tokenize(text)
    clean_sentences = cleanup_sentences(text)
    # for i, s in enumerate(raw_sentences):
    #     print(i, s)
    # for i, s in enumerate(clean_sentences):
    #     print(i, s)
    centroid_words = get_tf_idf(clean_sentences)
    # print(len(centroid_words), centroid_words)
    word_vectors = word_vectors_cache(clean_sentences, emdedding_model)
    #Centroid embedding representation
    centroid_vector = build_embedding_representation(centroid_words, word_vectors, emdedding_model)
    sentences_scores = []
    for i in range(len(clean_sentences)):
        scores = []
        words = clean_sentences[i].split()

        #Sentence embedding representation
        sentence_vector = build_embedding_representation(words, word_vectors, emdedding_model)

        #Cosine similarity between sentence embedding and centroid embedding
        score = similarity(sentence_vector, centroid_vector)
        sentences_scores.append((i, raw_sentences[i], score, sentence_vector))
    sentence_scores_sort = sorted(sentences_scores, key=lambda el: el[2], reverse=True)
    count = 0
    sentences_summary = []
    #Handle redundancy
    for s in sentence_scores_sort:
        if count > 100:
            break
        include_flag = True
        for ps in sentences_summary:
            sim = similarity(s[3], ps[3])
            if sim > 0.95:
                include_flag = False
        if include_flag:
            sentences_summary.append(s)
            count += len(s[1].split())

        sentences_summary = sorted(sentences_summary, key=lambda el: el[0], reverse=False)

    summary = "\n".join([s[1] for s in sentences_summary])
    return summary
def summarAndsend(chat_id,text):
     if text=="/start":
      a=welcome
     else:    
      clean_sentences = cleanup_sentences(text)
      words = []
      for sent in clean_sentences:
        words.append(nlkt_word_tokenize(sent))
      model = Word2Vec(words, min_count=1, sg = 1)
      a = summarize(text, model)
     
     requests.get("https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+chat_id+"&text="+a)



while(1):
    req = requests.get("https://api.telegram.org/bot"+bot_token+"/getUpdates")
    if "result" in json.loads(req.content):
         content = json.loads(req.content)["result"]
         for i in range(n,len(content)):
           if "text" in content[i]["message"]:
             print(i)
             chat_id = str(content[i]["message"]["chat"]["id"])
             text = content[i]["message"]["text"]
             
           elif "document" in content[i]["message"]:
             chat_id = str(content[i]["message"]["chat"]["id"])
             file_id = content[i]["message"]["document"]["file_id"]  
             docreq = requests.get("https://api.telegram.org/bot"+bot_token+"/getFile?file_id="+file_id)
             file_path = json.loads(docreq.content)["result"]["file_path"]
             print(file_path)
             getPaper("https://api.telegram.org/bot"+bot_token+"/"+file_path,filename="random_paper.pdf"+str(i))
             paperFilePath = "random_paper.pdf"+str(i)
             paperContent = pdfplumber.open(paperFilePath).pages
             text = ""
             for page in paperContent:    
                text = text + " " +page.extract_text() 
           summarAndsend(str(chat_id),text)    
           n=n+1
           print(n)
    time.sleep(2);   
    
