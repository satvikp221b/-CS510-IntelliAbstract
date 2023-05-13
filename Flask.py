from flask import Flask, request
from flask_cors import CORS
import spacy
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS
import re
from rouge import Rouge


#Getting the stop words and punctuations as a list
stop_words=list(STOP_WORDS)

#Define the position tag that are allowed in the summary
pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

#Takes text as input and tokenizes and return it
def tokenizer(text):
    #Not using the large version as it takes a greater amount of time to load
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text.lower() for token in doc if token.pos_ in pos_tag]
    return tokens,doc

#Cleaning the text by removiing stop words and punctiation
def stop_word_and_punct_removal(tokens,stop_words,punctuation):
    clean_tokens=[]
    for token in tokens:
        if token not in (stop_words and punctuation):
            clean_tokens.append(token)
    return clean_tokens

#Taking the clean tokens and forming a word frequency dictionary that counts the occurence of the words in the token
def word_frequency(clean_tokens):
    word_freq_dict={}
    for token in clean_tokens:
        if token not in word_freq_dict.keys():
            word_freq_dict[token]=1
        else:
            word_freq_dict[token]+=1
    return word_freq_dict
 
#Taking the word frequency dictionary and normalizing it by dividing each value by the maximum frequency of any word in the dictionary
def normalizing_word_freq_dict(word_freq_dict):
    max_f=max(word_freq_dict.values())
    for word in word_freq_dict:
        word_freq_dict[word]/=max_f
    return word_freq_dict

#Getting the sentence strength by adding up all the words values for each sentence and storing it in a dictionary
def get_sentence_strength(doc,normalized_word_freq_dict):
    sentence_strength={}
    for sentence in doc.sents:
        for word in sentence:
            if word.text in normalized_word_freq_dict.keys():
                if sentence in sentence_strength:
                    sentence_strength[sentence]+=normalized_word_freq_dict[word.text]
                else:
                    sentence_strength[sentence]=normalized_word_freq_dict[word.text]
    return sentence_strength

app = Flask(__name__)
CORS(app)
@app.route('/',methods=['GET','POST'])
def index():
    global text,summary
    #Getting the text of the webpage where the extension is called from content.js as a POST 
    data=request.form.to_dict()

    if not data:
        return "No data received in the POST request"
        
    #Converting from JSON to dictionary and finally just keeping the key
    text=list(data.keys())[0]

    tokens,doc=tokenizer(text)
    clean_tokens=stop_word_and_punct_removal(tokens, stop_words, punctuation)
    word_freq_dict=word_frequency(clean_tokens)
    normalized_word_freq_dict=normalizing_word_freq_dict(word_freq_dict)
    sentence_strength=get_sentence_strength(doc,normalized_word_freq_dict)
    
    #Sorting the sentence strength dictionary by descending order of its value/strength
    sentence_strength_sorted = sorted(sentence_strength.items(), key=lambda value: value[1], reverse=True)
    summary = []
    
    #Calculating the number of sentences present in the original text
    number_of_sents=len(sentence_strength)

    no_of_sents_summary=0.2*number_of_sents
    for i in range(int(no_of_sents_summary)): 
        sentence=str(sentence_strength_sorted[i][0])
        no_words=sentence.split(' ')
        if len(no_words)<5 or len(sentence)<20:
            continue
        else:
            summary.append(sentence.capitalize())
 
    summary=''.join(summary)
    summary=re.sub("(\[\d\])", "", summary)

    #print(summary)
    rouge = Rouge()

    scores_1 = rouge.get_scores(summary, text)

    #print(scores_1)
    return summary
        

if __name__ == '__main__':
    app.run(port=8000) 


    