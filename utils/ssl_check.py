import ssl
import socket
import tldextract

def check_ssl(url):
    try:
        ext = tldextract.extract(url)
        hostname = f"{ext.domain}.{ext.suffix}"

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        return "Valid SSL Certificate"

    except Exception:
        return "Invalid or No SSL"