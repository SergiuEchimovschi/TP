# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

import time
import requests
import urllib.parse
import re
import html.parser
import hashlib
import json
import socket
import ssl
import datetime

# 35. Exercitiul 35
print("--- Exercitiul 35 ---")
parsed = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("scheme:", parsed.scheme)
print("netloc:", parsed.netloc)
print("path:", parsed.path)
print("query:", parsed.query)
print("fragment:", parsed.fragment)

time.sleep(1)

# 36. Exercitiul 36
print("\n--- Exercitiul 36 ---")
for link in ["/about", "contact.html", "../index.html"]:
    print("URL complet:", urllib.parse.urljoin(BASE_URL, link))

time.sleep(1)

# 37. Exercitiul 37
def extract_links(html_content: str) -> list:
    """Extrage toate legaturile unice din codul HTML folosind expresii regulate."""
    links = re.findall(r'href="([^"]+)"', html_content)
    return list(set(links))

r_main = requests.get(BASE_URL, timeout=TIMEOUT)
print("\n--- Exercitiul 37 ---")
print("Numar legaturi unice extrase:", len(extract_links(r_main.text)))

time.sleep(1)

# 38. Exercitiul 38
def split_links(links: list, domain: str) -> tuple:
    """Imparte legaturile in doua liste: interne si externe."""
    internal = []
    external = []
    parsed_domain = urllib.parse.urlparse(domain).netloc
    for link in links:
        full_url = urllib.parse.urljoin(domain, link)
        netloc = urllib.parse.urlparse(full_url).netloc
        if netloc == parsed_domain or netloc == "":
            internal.append(link)
        else:
            external.append(link)
    return internal, external

# 39. Exercitiul 39
class ImageFinder(html.parser.HTMLParser):
    """Parser HTML pentru extragerea atributului src din tagurile img."""
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src_val = dict(attrs).get("src")
            if src_val:
                self.images.append(src_val)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("\n--- Exercitiul 39 ---")
print("Testul pentru ImageFinder a trecut cu succes!")

finder_real = ImageFinder()
finder_real.feed(r_main.text)
print(len(finder_real.images), "imagini gasite pe pagina reala.")

time.sleep(1)

# 40. Exercitiul 40
def page_fingerprint(url: str) -> str:
    """Returneaza amprenta SHA-256 a continutului paginii."""
    r = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(r.content).hexdigest()

print("\n--- Exercitiul 40 ---")
print("Amprenta paginii:", page_fingerprint(BASE_URL))

time.sleep(1)

# 41. Exercitiul 41
print("\n--- Exercitiul 41 ---")
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(r_main.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)
    print("Antet Server din JSON incarcat:", loaded_headers.get("Server"))

# 42. Exercitiul 42
def resolve(hostname: str) -> str:
    """Returneaza adresa IP pentru un nume de gazda."""
    return socket.gethostbyname(hostname)

print("\n--- Exercitiul 42 ---")
print("Adresa IP pentru cybercor.org:", resolve("cybercor.org"))

# 43. Exercitiul 43
def cert_days_left(hostname: str) -> int:
    """Returneaza cate zile mai sunt pana la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_seconds = ssl.cert_time_to_seconds(cert["notAfter"])
            current_seconds = datetime.datetime.now(datetime.timezone.utc).timestamp()
            return int((expire_seconds - current_seconds) / (60 * 60 * 24))

print("\n--- Exercitiul 43 ---")
print("Zile ramase pana la expirarea certificatului:", cert_days_left("cybercor.org"))