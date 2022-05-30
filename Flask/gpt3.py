import openai
import wget
import pathlib
import pdfplumber
import numpy as np
#For downloading the pdf using link
def getPaper(paper_url, filename="random_paper.pdf"):
    """
    Downloads a paper from it's arxiv page and returns
    the local path to that file.
    """
    downloadedPaper = wget.download(paper_url, filename)    
    downloadedPaperFilePath = pathlib.Path(downloadedPaper)

    return downloadedPaperFilePath

getPaper('https://www.skola-auto.cz/wp-content/uploads/2017/04/General_topics.pdf',filename="random_paper.pdf")
paperFilePath = "random_paper.pdf"
paperContent = pdfplumber.open(paperFilePath).pages

def displayPaperContent(paperContent, page_start=0, page_end=5):
    for page in paperContent[page_start:page_end]:
        print(page.extract_text())
displayPaperContent(paperContent)

def showPaperSummary(paperContent):
    tldr_tag = "\n tl;dr:"
    openai.organization = 'Your-organisation-key'
    openai.api_key = "Your-api-key"
    engine_list = openai.Engine.list() # calling the engines available from the openai api 
    
    for page in paperContent:    
        text = page.extract_text() + tldr_tag
        response = openai.Completion.create(engine="davinci",prompt=text,temperature=0.3,
            max_tokens=140,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )
        print(response["choices"][0]["text"])

#for pdf upload
import pdfplumber

def extract_input_text(file_object):
    text = ""
    with pdfplumber.open(file_object) as pdf:
        for page in pdf.pages:
            text = text + page.extract_text() + " "
    return text

def post_processing(response_text):
    # Incomplete sentence removal - splice until last index of fullstop
    try:
        fullstop_index = response_text.rindex('.')
        response_text = response_text[:fullstop_index + 1]
    except Exception as e:
        print(e)
    return response_text.replace('\\n', '')

tldr_tag = "\n tl;dr:"

OPENAI_API_KEY = "Your-api-key"
openai.api_key = OPENAI_API_KEY#os.getenv("OPENAI_API_KEY")
openai.organization = "your-organisation-key"
openai.api_key = 'your-api-key'
engine_list = openai.Engine.list() # calling the engines available  # from the openai api

for page in paperContent:    
        text = page.extract_text() + tldr_tag

response = openai.Completion.create(engine="davinci",prompt=text,temperature=0.3,
            max_tokens=140,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )
print(response["choices"][0]["text"])

paperContent = pdfplumber.open(paperFilePath).pages
showPaperSummary(paperContent)