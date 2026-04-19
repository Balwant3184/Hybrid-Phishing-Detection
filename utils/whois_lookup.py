import whois
from datetime import datetime
from urllib.parse import urlparse

def get_domain_age(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        if domain.startswith("www."):
            domain = domain.replace("www.", "")

        w = whois.whois(domain)
        creation_date = w.creation_date

        # If list → take first
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return "Unknown"

        # 🔥 FIX: Remove timezone info if present
        if creation_date.tzinfo is not None:
            creation_date = creation_date.replace(tzinfo=None)

        now = datetime.now()

        age_days = (now - creation_date).days
        return f"{age_days} days"

    except Exception as e:
        print("WHOIS ERROR:", e)
        return "WHOIS Error"