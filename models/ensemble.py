import joblib
import numpy as np

# Load trained Random Forest model
model = joblib.load("models/saved_models/rf_model.pkl")

def predict_url(features_dict):

    feature_order = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "NoOfSubDomain",
    "IsHTTPS",
    "HasObfuscation",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL"
]

    # Convert dict → ordered list
    features = [features_dict.get(f, 0) for f in feature_order]

    features_array = np.array([features])

    prediction = model.predict(features_array)[0]
    probability = model.predict_proba(features_array)[0][1]

    risk_score = round(probability * 100, 2)

    result = "Phishing" if prediction == 1 else "Legitimate"

    # Feature importance
    importance = dict(
        zip(feature_order, model.feature_importances_)
    )

    return result, risk_score, importance