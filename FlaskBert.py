import torch
from transformers import BertTokenizer, BertModel
from flask import Flask, request
from flask_cors import CORS
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from rouge import Rouge
from summarizer import Summarizer


app = Flask(__name__)

MODEL_NAME = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)

def get_sentence_embeddings(sentences):
    embeddings = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", max_length=128, truncation=True, padding="max_length")
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())

    return embeddings

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

    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    sentence_embeddings = get_sentence_embeddings(sentences)

    n_clusters = min(3, len(sentences))
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=0).fit(sentence_embeddings)

    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sentence_embeddings)
    closest.sort()

    summary = ". ".join([sentences[i] for i in closest])

    # model = Summarizer()
    # result = model(text, min_length=60)
    # full = ''.join(result)

    rouge = Rouge()

    scores_2 = rouge.get_scores(summary, text)

    #print(scores_2)
    return summary

if __name__ == '__main__':
    app.run(port=8000) 


    