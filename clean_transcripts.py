import pandas as pd
import re

file_path = "C:\\Users\\lclai\\Desktop\\dementia_db.csv"  
data = pd.read_csv(file_path)

transcripts = data['transcript']


def preprocess_transcript(text):
    # Eliminar líneas del investigador (INV)
    text = re.sub(r"INV:.*?▶", "", text)  # Remover cualquier línea que empiece con INV
    
    # Eliminar etiqueta "PAR:"
    text = re.sub(r"PAR: ", "", text)  # Quitar "PAR: " al inicio de las líneas
    
    # Eliminar contenido entre corchetes []
    text = re.sub(r"\[.*?\]", "", text)
    
    # Eliminar caracteres "raros" como â–¶, â€¡, y similares
    text = re.sub(r"[^\w\s.,]", "", text)  # Conserva solo letras, números, espacios, puntos y comas
    
    # Quitar espacios extra
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Aplicar la función a todas las transcripciones
data['clean_transcripts'] = transcripts.apply(preprocess_transcript)

# Guardar el resultado en un nuevo CSV
output_file = "transcripts_cleaned.csv"
data.to_csv(output_file, index=False)

print(f"Transcripciones procesadas y guardadas en {output_file}")