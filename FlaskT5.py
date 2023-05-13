import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request
from flask_cors import CORS
from rouge import Rouge

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
    model_name = 't5-base'
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = T5Tokenizer.from_pretrained(model_name)

    def chunk_text(text, chunk_size=512):
        words = text.split(' ')
        chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        return chunks

    chunks = chunk_text(text)

    summaries = []
    for chunk in chunks:
        inputs = tokenizer.encode("summarize: " + chunk, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(outputs[0])
        summaries.append(summary)

    final_summary = ' '.join(summaries)

    rouge = Rouge()

    scores_3 = rouge.get_scores(final_summary, text)

    #print(scores_3)
    return final_summary

if __name__ == '__main__':
    app.run(port=8000) 


    