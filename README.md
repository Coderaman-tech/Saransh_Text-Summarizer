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
| `Bot_Token` | **Required** Telegram Bot Token |   

You need to import these libraries, if not downloaded use pip install
```bash
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
 
## Bot_Test
 ```bash
    cd Bot
    Add Telegram_Bot token in line number 20
    python3 index.py
 ```   
