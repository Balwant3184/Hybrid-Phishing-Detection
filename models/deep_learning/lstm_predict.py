import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

# Safe path loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "lstm_model.h5")
tokenizer_path = os.path.join(BASE_DIR, "tokenizer.pkl")

model = load_model(model_path)

with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

max_len = 200

def predict_lstm(url):
    seq = tokenizer.texts_to_sequences([url])
    padded = pad_sequences(seq, maxlen=max_len)
    prediction = model.predict(padded, verbose=0)[0][0]
    return float(prediction * 100)