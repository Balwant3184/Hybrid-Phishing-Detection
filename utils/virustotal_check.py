import requests
import base64

API_KEY = "58683b20919294b62e9d88c2dfe60d0fec3ced79d2f146bcb1d4d0d066f2264d"

def check_virustotal(url):
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        headers = {
            "x-apikey": API_KEY
        }

        response = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            malicious = data["data"]["attributes"]["last_analysis_stats"]["malicious"]
            suspicious = data["data"]["attributes"]["last_analysis_stats"]["suspicious"]

            return {
                "malicious": malicious,
                "suspicious": suspicious
            }
        else:
            return {"error": "Not Found"}

    except Exception as e:
        return {"error": str(e)}