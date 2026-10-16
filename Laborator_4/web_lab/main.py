# Laborator: functii, metode si importuri pe web
# Student: Echimovschi Sergiu

import argparse
import webtools

def main():
    parser = argparse.ArgumentParser(description="Genereaza un raport web folosind modulul webtools.")
    parser.add_argument("url", type=str, help="URL-ul țintă de analizat (ex: https://cybercor.org)")
    args = parser.parse_args()

    print("Constantă importată DEFAULT_HEADERS:", webtools.DEFAULT_HEADERS)
    webtools.site_report(args.url)

if __name__ == "__main__":
    main()