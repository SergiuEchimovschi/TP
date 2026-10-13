import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        return f"https://{host}{path}"
    else:
        return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except Exception as e:
        print(f"Error: {e}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "unknown")
        content_type = response.headers.get("Content-Type", "").split(";")[0]
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": server,
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    success_count = 0
    fail_count = 0

    for site in SITES:
        res = check_site(site)
        status = res.get("status")
        if status == 200:
            success_count += 1
            length = res.get("length", 0)
            results.append((site, length))
            print(f"{site} -> 200, {length} octeți")
        else:
            fail_count += 1

    results.sort(key=lambda x: x[1], reverse=True)
    print(f"Reuşite: {success_count} Eşuate: {fail_count}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []
        
        for h in SECURITY_HEADERS:
            if h.lower() in headers_lower:
                present.append(h)
            else:
                missing.append(h)
                
        score = int((len(present) / len(SECURITY_HEADERS)) * 100)
        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None
    
    for i in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            
            if last_status < 500:
                return {"status": last_status, "attempts": i}
        except requests.RequestException as e:
            last_error = str(e)
            last_status = None
            
    result = {"status": last_status, "attempts": attempts}
    if last_error:
        result["error"] = last_error
    return result