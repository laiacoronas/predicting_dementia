import os
import pandas as pd
import re

cha_folder = r"C:\Users\lclai\Desktop\Lu\Dementia"

def clean_transcript(text):

    lines = [line.strip() for line in text.split("\n") if line.startswith("*PAR:") or line.startswith("*INV:")]

    clean_lines = []
    for l in lines:
        prefix = "PAR:" if l.startswith("*PAR:") else "INV:" 
        l = re.sub(r"[*][A-Z]+:\s*", "", l)       
        l = re.sub(r"\[.*?\]", "", l)            
        l = re.sub(r"\s+", " ", l)               
        l = l.strip()
        if l:
            clean_lines.append(f"{prefix} {l} ▶")
    return " ".join(clean_lines)


data = []

for file in os.listdir(cha_folder):
    if file.endswith(".cha"):
        path = os.path.join(cha_folder, file)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        subject = re.findall(r"\d+", file)[0] if re.findall(r"\d+", file) else None
        id_line = re.search(r"@ID:.*\|PAR\|([^|]*)\|([^|]*)\|([^|]*)\|", text)
        age, sex, label = None, None, None
        if id_line:
            parts = id_line.group(0).split("|")
            if len(parts) > 3:
                age = parts[3].replace(";", ".").replace(".", "").strip()
                try:
                    age = int(age)
                except:
                    age = None
            if len(parts) > 4:
                sex = parts[4].strip()
            if len(parts) > 5:
                label = parts[5].strip()
        transcript = clean_transcript(text)

        data.append({
            "subject": subject,
            "age": age,
            "sex": sex,
            "label": label,
            "transcript": transcript
        })

df = pd.DataFrame(data)
df = df.dropna(subset=["transcript"]).reset_index(drop=True)
output_path = os.path.join(cha_folder, "pitt_clean.csv")
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"Dataset guardado en: {output_path}")
print(df.head())
