# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

import time
import requests

# 9. Exercitiul 9
response = requests.get(BASE_URL + "/", timeout=TIMEOUT)
print("status_code:", response.status_code)  # atribut
print("ok:", response.ok)                    # atribut
print("url:", response.url)                  # atribut
print("encoding:", response.encoding)        # atribut

time.sleep(1)

# 10. Exercitiul 10
try:
    response.raise_for_status()
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError:
    print("Eroare HTTP: pagina nu a fost gasita, dar exceptia a fost prinsa cu succes.")

time.sleep(1)

# 11. Exercitiul 11
for name, value in response.headers.items():
    print(name + ": " + value)

time.sleep(1)

# 12. Exercitiul 12
print("Server:", response.headers.get("Server", "lipseste"))
print("Content-Type:", response.headers.get("Content-Type", "lipseste"))
print("content-type litere mici:", response.headers.get("content-type", "lipseste"))
# Observație: Metoda .get() pe antete este insensibilă la majuscule și minuscule.

time.sleep(1)

# 13. Exercitiul 13
cyber_count = response.text.lower().count("cyber")
print("Aparitii cuvant cyber:", cyber_count)
# Putem înlănțui .lower() și .count() deoarece .lower() returnează un șir de caractere nou, iar pe acel șir nou putem apela direct .count().

# 14. Exercitiul 14
html_content = response.text
start = html_content.find("<title>") + len("<title>")
end = html_content.find("</title>")
if start != -1 and end != -1:
    print("Titlu extras:", html_content[start:end].strip())

# 15. Exercitiul 15
lines = html_content.splitlines()
print("Numar linii:", len(lines))
print("Lungime cea mai lunga linie:", len(max(lines, key=len)))

# 16. Exercitiul 16
if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")

time.sleep(1)

# 17. Exercitiul 17
redirect_res = requests.get("http://cybercor.org", timeout=TIMEOUT)
for h in redirect_res.history:
    print("Redirectionare status:", h.status_code, "URL:", h.url)
print("URL final:", redirect_res.url)

time.sleep(1)

# 18. Exercitiul 18
head_res = requests.head(BASE_URL + "/", timeout=TIMEOUT)
get_res = requests.get(BASE_URL + "/", timeout=TIMEOUT)
print("Lungime continut HEAD:", len(head_res.content))
print("Lungime continut GET:", len(get_res.content))
# O cerere HEAD returnează doar antetele fără corpul paginii (de aceea lungimea conținutului este 0), în timp ce cererea GET returnează și conținutul complet.

time.sleep(1)

# 19. Exercitiul 19
if len(response.cookies) == 0:
    print("Niciun cookie setat.")
else:
    for cookie in response.cookies:
        print("Cookie:", cookie.name, "Secure:", cookie.secure)

time.sleep(1)

# 20. Exercitiul 20
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Echim"})
session_res = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Raspuns echo headers:", session_res.json())