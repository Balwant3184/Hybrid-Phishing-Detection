import re
import tldextract

def extract_features(url):

    features = {}

    ext = tldextract.extract(url)
    domain = ext.domain

    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain)
    features["IsDomainIP"] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    features["NoOfSubDomain"] = len(ext.subdomain.split(".")) if ext.subdomain else 0
    features["IsHTTPS"] = 1 if url.startswith("https") else 0
    features["HasObfuscation"] = 1 if "%" in url else 0

    digits = sum(c.isdigit() for c in url)
    features["NoOfDegitsInURL"] = digits
    features["DegitRatioInURL"] = digits / len(url) if len(url) > 0 else 0

    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")

    special_chars = len(re.findall(r"[^\w]", url))
    features["NoOfOtherSpecialCharsInURL"] = special_chars
    features["SpacialCharRatioInURL"] = special_chars / len(url) if len(url) > 0 else 0

    return features