from summarizer import Summarizer
from rouge_score import rouge_scorer
import pandas as pd

#replace this with your our summarizer
model = Summarizer()
result = model(body, min_length=60)
full = ''.join(result)
print(full)

# Load the dataset
df = pd.read_csv('test.csv', encoding='utf-8') #replace this with your own dataset

# Initialize the summarizer
model = Summarizer()

# Initialize the ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Evaluate each article
rouge1_scores = []
rouge2_scores = []
rougeL_scores = []
f1_scores = []

for index, row in df.iterrows():
    # Get the article and target summary
    article = row['article']
    target_summary = row['highlights']

    result = model(article, min_length=60)
    summary = ''.join(result)
    # Generate the summary using the summarizer
    #summary = model(article, num_sentences=3)
    
    # Calculate the ROUGE and F1 scores
    scores = scorer.score(target_summary, summary)
    
    rouge1_scores.append(scores['rouge1'].fmeasure)
    rouge2_scores.append(scores['rouge2'].fmeasure)
    rougeL_scores.append(scores['rougeL'].fmeasure)
    f1_scores.append((2 * scores['rouge1'].fmeasure * scores['rouge2'].fmeasure) / (scores['rouge1'].fmeasure + scores['rouge2'].fmeasure))

# Print the average scores
print('ROUGE-1 F1 Score:', sum(rouge1_scores) / len(rouge1_scores))
print('ROUGE-2 F1 Score:', sum(rouge2_scores) / len(rouge2_scores))
print('ROUGE-L F1 Score:', sum(rougeL_scores) / len(rougeL_scores))
print('F1 Score:', sum(f1_scores) / len(f1_scores))
