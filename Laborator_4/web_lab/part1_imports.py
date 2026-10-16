
# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import requests
import urllib.request

# 1. Exercițiul 1. Primul import
print("--- Exercitiul 1 ---")
print("Versiune requests:", requests.__version__)
# Explicatie: 'requests' a avut nevoie de 'pip install' deoarece este o biblioteca externa 
# (nu face parte din biblioteca standard Python), in timp ce 'urllib.request' face parte 
# din biblioteca standard Python si este instalata automat odata cu interpretorul.

# 2. Exercițiul 2. Două stiluri de import
print("\n--- Exercitiul 2 ---")
response1 = requests.get(BASE_URL + "/", timeout=TIMEOUT)
print("Cod de stare (requests.get):", response1.status_code)

from requests import get
response2 = get(BASE_URL + "/", timeout=TIMEOUT)
print("Cod de stare (from requests import get):", response2.status_code)
# Comentariu (avantaje): 
# - import requests: Evita conflictele de nume si arata clar provenienta functiei (requests.get).
# - from requests import get: Permite scrierea mai scurta a codului, apeland direct functia get().

# 3. Exercițiul 3. Alias-uri
print("\n--- Exercitiul 3 ---")
import requests as rq
response3 = rq.get(BASE_URL + "/", timeout=TIMEOUT)
print("Cod de stare cu alias rq:", response3.status_code)
# Comentariu: Un alias face codul mai usor de citit atunci cand numele modulului este lung 
# sau frecvent utilizat, dar il poate face mai greu de citit daca aliasul este neobisnuit 
# sau obscur pentru alti programatori.

# 4. Exercițiul 4. Doar biblioteca standard
print("\n--- Exercitiul 4 ---")
req = urllib.request.Request(
    BASE_URL + "/", 
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req) as conn:
    print("Atribut .status:", conn.status)
    body_snippet = conn.read(200).decode("utf-8")
    print("Primele 200 caractere din corp:", body_snippet)

# 5. Exercițiul 5. Priviți în interiorul unui modul
print("\n--- Exercitiul 5 ---")
print("Primele 5 elemente din dir(requests):", dir(requests)[:5])
# Comentariu: 
# - requests.get este o functie (metoda helper).
# - requests.Session este o clasa.
# - requests.exceptions este un modul (contine exceptiile bibliotecii).

# 6. Exercițiul 6. Citiți documentația
print("\n--- Exercitiul 6 ---")
# help(requests.get) # Decomenteaza daca doresti sa afisezi documentatia in terminal
response_timeout = requests.get(BASE_URL + "/", timeout=TIMEOUT)
print("Cerere efectuata cu succes folosind parametrul timeout:", response_timeout.status_code)

# 7. Exercițiul 7. Cronometrarea unei cereri
print("\n--- Exercitiul 7 ---")
start_perf = time.perf_counter()
res_perf = requests.get(BASE_URL + "/", timeout=TIMEOUT)
end_perf = time.perf_counter()
print(f"Durata masurata cu time.perf_counter(): {end_perf - start_perf:.4f} secunde")
print(f"Durata raportata de response.elapsed: {res_perf.elapsed.total_seconds()} secunde")

# 8. Exercițiul 8. Când un import eșuează
print("\n--- Exercitiul 8 ---")
try:
    import bs4
    print("Modulul bs4 este instalat.")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")