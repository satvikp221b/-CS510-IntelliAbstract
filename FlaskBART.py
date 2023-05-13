from transformers import BartTokenizer, BartForConditionalGeneration
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

    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

    # Tokenize the input text
    inputs = tokenizer([text], max_length=1024, return_tensors='pt')

    # Generate the summary
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)

    # Decode the summary
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]

    rouge = Rouge()

    scores_4 = rouge.get_scores(summary, [text])

    #print(scores_4)
    return summary

if __name__ == '__main__':
    app.run(port=8000) 


    