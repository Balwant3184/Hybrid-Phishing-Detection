import random
import re

def generate_adversarial_variants(url):

    variants = []

    # 1️⃣ Replace 'l' with '1'
    variants.append(url.replace("l", "1"))

    # 2️⃣ Replace 'o' with '0'
    variants.append(url.replace("o", "0"))

    # 3️⃣ Add suspicious keyword
    variants.append(url + "-secure")

    # 4️⃣ Add random subdomain
    variants.append("http://verify-" + url.replace("https://", "").replace("http://", ""))

    # 5️⃣ Insert extra hyphen
    variants.append(url.replace(".", "-."))

    return list(set(variants))