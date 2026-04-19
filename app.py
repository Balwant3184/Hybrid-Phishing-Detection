from flask import Flask, render_template, request, jsonify
from utils.feature_extraction import extract_features
from utils.threat_intel import check_threat_intelligence
from utils.ssl_check import check_ssl
from utils.whois_lookup import get_domain_age
from utils.virustotal_check import check_virustotal
from utils.google_safe_browsing import check_google_safe_browsing
from models.deep_learning.lstm_predict import predict_lstm
import joblib
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

# ------------------ LOAD MODEL ------------------

model = joblib.load("optimized_model.pkl")

SELECTED_FEATURES = [
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

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

# ------------------ MAIN PREDICTION API ------------------

@app.route("/api/predict", methods=["GET", "POST"])
def api_predict():

    if request.method == "GET":
        return jsonify({"message": "API is working. Use POST to send URL."})

    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        # -------- Feature Extraction --------
        features = extract_features(url)
        optimized_features = [features.get(f, 0) for f in SELECTED_FEATURES]

        # -------- ML Probability --------
        prob = model.predict_proba([optimized_features])[0][1]
        ml_score = round(prob * 100, 2)

        # -------- LSTM Score --------
        lstm_score = predict_lstm(url)

        # -------- External Security Checks --------
        threat_data = check_threat_intelligence(url)
        ssl_status = check_ssl(url)
        domain_age = get_domain_age(url)
        vt_result = check_virustotal(url)
        google_safe = check_google_safe_browsing(url)

        google_safe_status = google_safe.get("status") if isinstance(google_safe, dict) else "Unknown"
        vt_malicious = vt_result.get("malicious", 0) if isinstance(vt_result, dict) else 0
        vt_suspicious = vt_result.get("suspicious", 0) if isinstance(vt_result, dict) else 0

        # ------------------ STABLE FINAL SCORING ENGINE ------------------

        external_score = 0

        # Google Safe Browsing
        if google_safe_status == "Malicious":
            external_score += 100

        # VirusTotal
        if vt_malicious > 0:
            external_score += 80
        elif vt_suspicious > 0:
            external_score += 40

        # Weighted Risk Calculation
        risk_score_final = (
            (0.6 * ml_score) +
            (0.3 * external_score) +
            (0.1 * lstm_score)
        )

        # Clamp score between 0–100
        risk_score_final = round(min(max(risk_score_final, 0), 100), 2)

        # -------- Final Classification --------
        if risk_score_final >= 70:
            prediction_label = "Phishing"
        elif risk_score_final >= 40:
            prediction_label = "Suspicious"
        else:
            prediction_label = "Secure"

        # -------- Feature Importance --------
        importance_dict = {}
        try:
            importances = model.feature_importances_
            for i, feat in enumerate(SELECTED_FEATURES):
                importance_dict[feat] = round(float(importances[i]), 4)
        except:
            pass

        # -------- Response --------
        response = {
            "prediction": prediction_label,
            "risk_score": risk_score_final,
            "hybrid_score": risk_score_final,   # Used by frontend gauge
            "ml_score": ml_score,
            "lstm_score": lstm_score,
            "feature_importance": importance_dict,
            "threat_intelligence": threat_data or {},
            "ssl_status": ssl_status or "Unknown",
            "domain_age": domain_age or "Unknown",
            "virustotal": vt_result or {},
            "google_safe_browsing": google_safe or {"status": "Unknown"},
            "bpso_features": SELECTED_FEATURES
        }

        return jsonify(response)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)