import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Load dataset (CSV must have 'url' and 'label')
df = pd.read_csv("data/phishing_dataset.csv")
df.columns = df.columns.str.strip()   # safety

urls = df["URL"]
labels = df["label"]

# Tokenize characters
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(urls)

sequences = tokenizer.texts_to_sequences(urls)
max_len = 200
X = pad_sequences(sequences, maxlen=max_len)
y = labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=32, input_length=max_len))
model.add(LSTM(64))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))

model.save("lstm_model.h5")

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Model trained and saved.")