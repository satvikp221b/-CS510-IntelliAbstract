import torch
from transformers import BertTokenizer, BertModel
from flask import Flask, request
from flask_cors import CORS
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from rouge import Rouge
from summarizer import Summarizer


app = Flask(__name__)


CORS(app)
@app.route('/',methods=['GET','POST'])
def index():
    global text,summary

    data=request.form.to_dict()
    
    if not data:
        return "No data received in the POST request"
        
    text=list(data.keys())[0]
    #print(text)
    summary = summarization(text)

    return summary

def summarization(text):

    model = Summarizer()
    result = model(text, min_length=60)
    full = ''.join(result)

    rouge = Rouge()

    scores_2 = rouge.get_scores(full, text)

    return full

if __name__ == '__main__':
    app.run(port=8000) 


    