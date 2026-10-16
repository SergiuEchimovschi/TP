# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

BASE_URL = "https://cybercor.org"
TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Echim"}

import time
import requests
import socket
import ssl
import datetime
import json
import urllib.parse
import re
import csv

def fetch(url: str) -> requests.Response:
    """Descarca un URL folosind antetele implicite."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code

def get_title(html: str) -> str:
    """Primește un șir HTML și returnează titlul paginii extras."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return ""

def security_headers(url: str) -> dict:
    """Verifica prezenta celor 5 antete de securitate și returnează un dicționar."""
    r = fetch(url)
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    return {h: h in r.headers for h in headers_to_check}

def score_headers(results: dict) -> str:
    """Primeste dictionarul de securitate și returnează un scor de tip 'X/5'."""
    passed = sum(1 for val in results.values() if val)
    return f"{passed}/{len(results)}"

def resolve(hostname: str) -> str:
    """Returneaza adresa IP pentru un nume de gazda."""
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    """Returneaza cate zile mai sunt pana la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_seconds = ssl.cert_time_to_seconds(cert["notAfter"])
            current_seconds = datetime.datetime.now(datetime.timezone.utc).timestamp()
            return int((expire_seconds - current_seconds) / (60 * 60 * 24))

def fetch_robots(base: str) -> str | None:
    """Returneaza textul fisierului robots.txt sau None dacă lipseste."""
    try:
        r = fetch(base + "/robots.txt")
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

def site_report(url: str):
    """Genereaza raportul complet al site-ului, salveaza report.json si report.csv."""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.netloc

    http_url = f"http://{hostname}"
    try:
        redirect_res = requests.get(http_url, timeout=TIMEOUT)
        history_str = " -> ".join([str(h.status_code) for h in redirect_res.history] + [str(redirect_res.status_code)])
        final_url = redirect_res.url
    except requests.RequestException:
        history_str = "Indisponibil"
        final_url = url

    r = fetch(url)
    status = r.status_code
    title = get_title(r.text)
    ip_addr = resolve(hostname)
    sec_dict = security_headers(url)
    sec_score = score_headers(sec_dict)
    days_left = cert_days_left(hostname)

    all_links = re.findall(r'href="([^"]+)"', r.text)
    internal_count = 0
    external_count = 0
    for link in all_links:
        full = urllib.parse.urljoin(url, link)
        if urllib.parse.urlparse(full).netloc == hostname:
            internal_count += 1
        else:
            external_count += 1

    robots_txt = fetch_robots(f"{parsed.scheme}://{hostname}")
    disallowed = disallowed_paths(robots_txt)

    report_data = {
        "url": final_url,
        "status_code": status,
        "title": title,
        "ip_address": ip_addr,
        "redirects": history_str,
        "security_score": sec_score,
        "cert_days_left": days_left,
        "internal_links": internal_count,
        "external_links": external_count,
        "disallowed_paths": disallowed
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {status}")
    print(f"Titlu:             {title}")
    print(f"Adresă IP:         {ip_addr}")
    print(f"Redirecționări:    {history_str} -> {final_url}")
    print(f"Scor securitate:   {sec_score}")
    print(f"Certificat:        {days_left} de zile rămase")
    print(f"Legături:          {internal_count} interne, {external_count} externe")
    print(f"Căi interzise:     {', '.join(disallowed) if disallowed else 'Niciuna'}")

    # Salvare în report.json
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
    print("Salvat în report.json")

    # Salvare în report.csv (Exercițiul 49)
    with open("report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        checked_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for p in ["/", "/robots.txt", "/sitemap.xml"]:
            try:
                st = fetch(f"{parsed.scheme}://{hostname}{p}").status_code
            except:
                st = None
            writer.writerow([p, st, checked_at])
    print("Salvat în report.csv")