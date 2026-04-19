import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("data/phishing_dataset.csv")

# BPSO selected features
selected_features = [
'URLSimilarityIndex', 'CharContinuationRate', 'URLCharProb',
'NoOfSubDomain', 'ObfuscationRatio', 'NoOfLettersInURL',
'DegitRatioInURL', 'NoOfAmpersandInURL', 'IsHTTPS',
'LineOfCode', 'LargestLineLength', 'HasTitle',
'DomainTitleMatchScore', 'Robots', 'IsResponsive',
'NoOfURLRedirect', 'NoOfSelfRedirect', 'NoOfiFrame',
'HasExternalFormSubmit', 'Bank', 'Crypto',
'HasCopyrightInfo', 'NoOfCSS', 'NoOfJS',
'NoOfSelfRef', 'NoOfEmptyRef'
]

X = data[selected_features]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print("Optimized Model Accuracy:", acc)

# Save optimized model
joblib.dump(model, "optimized_model.pkl")
print("Model saved as optimized_model.pkl")