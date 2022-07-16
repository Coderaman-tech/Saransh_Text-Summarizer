#  Saransh- Text Summarizer

<img src="Media/Screenshot (499).png"></img><br>

In this project, we have made an automatic text summarizzer which summarizes different types of text data sources.

 We make the system to generate a summary of the text and provide a JSON output for the same. Alternatively, if there are web articles, PDFs, etc uploaded by the educator, the solution is able to summarize the large content into bite-sized information.


## API Reference

#### Get all items

```http
  https://openai.com/api/
```

| Parameter |Description                |
| :-------- |:------------------------- |
| `api_key` | **Required**. Your API key |
| `organisaton_key` |**Required**. Your Organisaton key |
| `Bot_Token | **Required** Telegram Bot Token |   

You need to import these libraries, if not downloaded use pip install
```bash
import openai
import wget
import pathlib
import pdfplumber
import numpy as np
from regex import W
import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import string
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize as nlkt_sent_tokenize
from nltk.tokenize import word_tokenize as nlkt_word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine
from flask import Flask, jsonify,request
import json
from flask_cors import CORS, cross_origin
```
## Tests



```bash
   cd Flask
   python3 index.py
   cd ./
   cd Express
   npm install
   npm run dev
```
 
##Bot_Test
 ```bash
    cd Bot
    Add Telegram_Bot token in line number 27
    python3 index3.py
 ```   
