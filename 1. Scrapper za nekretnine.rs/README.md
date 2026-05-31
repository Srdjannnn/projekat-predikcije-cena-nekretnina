# 🕷️ Scrapper za nekretnine.rs

Automatsko prikupljanje oglasa o nekretninama sa sajta nekretnine.rs korišćenjem Python web scraper tehnologije.

## 📋 Opis

Web scraper koji automatski ekstraktuje informacije o nekretninama (cijena, lokacija, kvadratura, vrsta nekretnine, itd.) i čuva ih u strukturiranom CSV formatu. Modul se može prilagoditi i za druge immobiliyenske sajtove.

## 🛠️ Arhitektura

```
scraper/
├── __init__.py           # Inicijalizacija paketa
├── config.py            # Konfiguracije (URL-ovi, parametri)
├── scraper.py           # Glavna logika skrapiranja
├── parser.py            # Parsiranje HTML-a
├── models.py            # Modeli podataka
└── save_data.py         # Čuvanje podataka u CSV

data/
└── raw/
    └── dataset.csv      # Skrapirani sirovinski podaci

outputs/
└── dataset.csv          # Obrađeni podaci (ako primjenjivo)
```

## 📦 Zavisnosti

Pogledajte `requirements.txt` za sve potrebne biblioteke:
- BeautifulSoup4 - HTML parsing
- Requests - HTTP zahtjeve
- Pandas - Rukovanje podacima
- I druge biblioteke...

## ⚙️ Instalacija

```bash
# 1. Instaliraj zavisnosti
pip install -r requirements.txt

# 2. Prilagodi config.py prema potrebi (ako je potrebno)
```

## 🚀 Pokretanje

```bash
# Metodan 1: Direktno pokretanje
python -m scraper.scraper

# Metodan 2: Iz root direktorijuma projekta
cd ..
python -m "1. Scrapper za nekretnine.rs".scraper.scraper
```

## 📊 Izlazni Podaci

Skrapirani podaci se čuvaju u `data/raw/dataset.csv` sa sledećim kolonama:

| Kolona | Opis |
|--------|------|
| price | Cijena nekretnine |
| location | Lokacija |
| area | Kvadratura |
| property_type | Vrsta nekretnine |
| ... | ... |

## ⚠️ Napomene

- Respectuj Terms of Service web-sajta
- Koristi odgovarajuće delay između zahtjeva
- Provjeri regulatorne zahtjeve za web scraping u vašoj zemlji
- Preporuka je ažuriranje podataka periodički

## 🔗 Sljedeći Korak

Nakon što se podaci skrapiraju, preidi na **Validacija podataka i preprocessing** fazu.

