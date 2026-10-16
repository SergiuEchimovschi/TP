# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

import time
import requests

# 21. Exercitiul 21
def fetch(url: str) -> requests.Response:
    """Descarca un URL si returneaza obiectul Response."""
    return requests.get(url, timeout=TIMEOUT)

print("--- Exercitiul 21 ---")
res_21 = fetch(BASE_URL + "/")
print("Cod de stare fetch:", res_21.status_code)

time.sleep(1)

# 22. Exercitiul 22
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print("\n--- Exercitiul 22 ---")
paths = ["/", "/robots.txt", "/sitemap.xml"]
for p in paths:
    code = get_status(BASE_URL + p)
    print(f"Path {p} -> Status: {code}")
    time.sleep(1)

# 23. Exercitiul 23
def fetch_with_timeout(url: str, timeout: int = 10) -> requests.Response:
    """Descarca un URL folosind un timeout specificat."""
    return requests.get(url, timeout=timeout)

print("\n--- Exercitiul 23 ---")
print("Fetch cu timeout implicit (10):", fetch_with_timeout(BASE_URL + "/").status_code)
time.sleep(1)
print("Fetch cu timeout personalizat (3):", fetch_with_timeout(BASE_URL + "/", timeout=3).status_code)

time.sleep(1)

# 24 & 25. Exercitiul 24 și 25
def get_title(html: str) -> str:
    """Primește un șir HTML și returnează titlul paginii extras."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return ""

print("\n--- Exercitiul 25 (Docstring) ---")
help(get_title)

# 26. Exercitiul 26
# Notă: Adnotările de tip oferă indicii despre tipuri, dar Python nu oprește rularea dacă trimiți un tip greșit.

# 27. Exercitiul 27
def page_exists(url: str) -> bool:
    """Returneaza True daca pagina exista si poate fi accesata, altfel False."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False

print("\n--- Exercitiul 27 ---")
print("Exista domeniul invalid?", page_exists("https://this-domain-does-not-exist.invalid"))

time.sleep(1)

# 28. Exercitiul 28
def check_paths(base: str, path_list: list) -> dict:
    """Primeste o lista de cai si returneaza un dictionar {path: status_code}."""
    results = {}
    for path in path_list:
        try:
            r = requests.get(base + path, timeout=TIMEOUT)
            results[path] = r.status_code
        except requests.RequestException:
            results[path] = None
        time.sleep(1)
    return results

print("\n--- Exercitiul 28 ---")
print("Verificare cai:", check_paths(BASE_URL, ["/", "/robots.txt"]))

# 29. Exercitiul 29
def get_header(url: str, name: str, default: str = "lipseste") -> str:
    """Returneaza valoarea unui singur antet dintr-un URL."""
    r = requests.get(url, timeout=TIMEOUT)
    return r.headers.get(name, default)

print("\n--- Exercitiul 29 ---")
print("Antet Server:", get_header(BASE_URL, name="Server"))

time.sleep(1)

# 30. Exercitiul 30
def security_headers(url: str) -> dict:
    """Verifica prezenta celor 5 antete de securitate si returneaza un dictionar."""
    r = requests.get(url, timeout=TIMEOUT)
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    return {h: h in r.headers for h in headers_to_check}

print("\n--- Exercitiul 30 ---")
print("Antete securitate:", security_headers(BASE_URL))

time.sleep(1)

# 31. Exercitiul 31
def score_headers(results: dict) -> str:
    """Primeste dictionarul de securitate si returneaza un scor de tip 'X/5'."""
    passed = sum(1 for val in results.values() if val)
    return f"{passed}/{len(results)}"

print("\n--- Exercitiul 31 ---")
print("Scor securitate:", score_headers(security_headers(BASE_URL)))

time.sleep(1)

# 32. Exercitiul 32
def fetch_robots(base: str) -> str | None:
    """Returneaza textul fisierului robots.txt sau None daca lipseste."""
    try:
        r = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        if r.status_code == 200:
            return r.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text: str | None) -> list:
    """Returneaza o lista cu toate valorile Disallow din robots.txt."""
    if not robots_text:
        return []
    disallowed = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                disallowed.append(path)
    return disallowed

print("\n--- Exercitiul 32 ---")
print("Cai interzise in robots.txt:", disallowed_paths(fetch_robots(BASE_URL)))

time.sleep(1)

# 33. Exercitiul 33
def response_times(*urls: str) -> dict:
    """Returneaza un dictionar cu timpii de raspuns {url: secunde} pentru URL-urile date."""
    times = {}
    for url in urls:
        start = time.perf_counter()
        try:
            requests.get(url, timeout=TIMEOUT)
            dur = time.perf_counter() - start
            times[url] = round(dur, 3)
        except requests.RequestException:
            times[url] = None
        time.sleep(1)
    return times

print("\n--- Exercitiul 33 ---")
print("Timpi de raspuns:", response_times(BASE_URL + "/", "https://httpbin.org/get"))

# 34. Exercitiul 34
def log(message: str, **details):
    """Afiseaza un mesaj urmat de fiecare detaliu cheie-valoare."""
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

print("\n--- Exercitiul 34 ---")
log("verificat", url=BASE_URL, status=200)