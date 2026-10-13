from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)

print("--- Partea 1: Funcții ---")
print("build_url normal:", build_url("example.com", "login"))
print("build_url cu slash:", build_url("example.com", "/login"))
print("is_https (True):", is_https("https://example.com"))
print("is_https (False):", is_https("http://example.com"))

print("\n--- Partea 2: Trimiterea unei cereri ---")
show_response("https://example.com")

print("\n--- Partea 3: Un verificator reutilizabil ---")
print("check_site (succes):", check_site("https://example.com"))
print("check_site (eroare):", check_site("http://this-site-does-not-exist.invalid"))

print("\n--- Partea 4: Verificarea mai multor site-uri ---")
scan_sites()

print("\n--- Partea 5: Audit de securitate ---")
print("check_headers:", check_headers("https://example.com"))

print("\n--- Partea 6: Încercări repetate ---")
print("retry_check 200:", retry_check("https://httpbin.org/status/200"))
print("retry_check 404:", retry_check("https://httpbin.org/status/404"))
print("retry_check 500:", retry_check("https://httpbin.org/status/500", attempts=2))