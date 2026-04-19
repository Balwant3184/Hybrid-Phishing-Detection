import requests
import os

API_KEY = "AIzaSyAsWyzodvQvwpkfEMC9PlmE9WUmNP9y-gI"

def check_google_safe_browsing(url):
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client": {
            "clientId": "phishguard",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
        result = response.json()

        if "matches" in result:
            return {
                "status": "Malicious",
                "details": result["matches"]
            }
        else:
            return {
                "status": "Safe",
                "details": None
            }

    except Exception as e:
        return {
            "status": "Error",
            "details": str(e)
        }