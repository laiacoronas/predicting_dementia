import pandas as pd
import re

file_path = "C:\\Users\\lclai\\Desktop\\dementia_db.csv"  
data = pd.read_csv(file_path)

transcripts = data['transcript']


def preprocess_transcript(text):
    
    text = re.sub(r"INV:.*?▶", "", text)  
    
    text = re.sub(r"PAR: ", "", text)  
    
    text = re.sub(r"\[.*?\]", "", text)
    
    text = re.sub(r"[^\w\s.,]", "", text)  
    
    text = re.sub(r"\s+", " ", text).strip()
    return text

data['clean_transcripts'] = transcripts.apply(preprocess_transcript)

output_file = "transcripts_cleaned.csv"
data.to_csv(output_file, index=False)

print(f"Transcripciones procesadas y guardadas en {output_file}")