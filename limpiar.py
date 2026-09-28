from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tqdm import tqdm

pd.set_option("display.max_colwidth", None)
tqdm.pandas()

CARPETA_DATOS = Path(__file__).resolve().parent / "data"

#---- LECTURA ----

df = pd.read_csv(CARPETA_DATOS / "dataset.csv", keep_default_na=False)
print("Filas originales:", len(df))

#---- LIMPIEZA BÁSICA ----

print("label_text distinto de label:", (df["label"] != df["label_text"]).sum())
df = df.drop(columns="label_text")

#Nulos 
df = df.replace("", pd.NA)
print("Nulos por columna:")
print(df.isna().sum())
df = df.dropna()

#Textos vacíos 
vacios = df["text"].str.strip() == ""
print("Textos vacíos:", vacios.sum())
df = df[~vacios]

#Duplicados
print("Filas duplicadas:", df.duplicated().sum())
print("Ids duplicados:", df["id"].duplicated().sum())
print("Textos repetidos con distinto id (se conservan):", df["text"].duplicated().sum())
df = df.drop_duplicates()

print("Filas finales:", len(df))

#---- TOKENIZACIÓN Y PREPROCESADO ----

#Se conservan las negaciones porque cambian el sentido de la reseña ("not good").

NEGACIONES = {"not", "no", "nor", "never"}
STOPWORDS = set(stopwords.words("english")) - NEGACIONES

def preprocesar(texto):
    texto = texto.lower()
    for char in "1234567890.,!?:;'’\"":
        texto = texto.replace(char, "")
    tokens = word_tokenize(texto)
    tokensnew = []
    for token in tokens:
        if token not in STOPWORDS and len(token) > 1 and token not in ["''", "``"]:
            tokensnew.append(token)
    return " ".join(tokensnew) 

df["clean_text"] = df["text"].apply(preprocesar)

print(df[["text", "clean_text"]].head())

df.to_csv(CARPETA_DATOS / "dataset_limpio.csv", index=False, encoding="utf-8-sig")