# Preprocessing podataka

Cilj ovog dela projekta je da sirovi CSV iz `data/raw/dataset.csv` pretvori u dataset (kojije upotrebljiv modelima)  `data/processed/processed_dataset.csv`.



## Instalacija


python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Pokretanje prog

.\.venv\Scripts\python.exe -m src.preprocessing


Pipeline ima funkcije da:

- validaciju kolona
- uklanjanje duplikata
- obradu vrednosti koje fale
- ciscenje numerickih i tekstualnih kolona
- uklanjanje outliera IQR metodom za `price` i `area`
- feature engineering
- Output finalnog CSV dataseta

## FeatureEngineering

Dodaju se:

- `price_per_m2`
- `building_age`
- `floor_ratio`
- binarne vrednosti za `elevator`, `terrace`, `parking`
- one-hot encoding za `city` i `municipality`