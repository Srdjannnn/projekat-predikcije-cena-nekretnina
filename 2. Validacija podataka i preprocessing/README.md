# 🔍 Validacija Podataka i Preprocessing

Transformacija sirovih skrapiranih podataka u čist, strukturiran dataset spreman za machine learning modele.

## 📋 Opis

Ovaj modul obavlja ključne korake obrade podataka:
- Validaciju integriteta podataka
- Čišćenje i normalizaciju
- Rukovanje nedostajućim vrijednostima
- Feature engineering za poboljšane modele

## 🛠️ Arhitektura

```
├── __init__.py              # Inicijalizacija paketa
├── data_validation.py       # Validacija podataka
├── preprocessing.py         # Glavna obrada
├── features.py             # Feature engineering
├── utils.py                # Pomoćne funkcije
├── dataset.csv             # Ulazni podaci
└── processed_dataset.csv   # Izlazni obrađeni podaci
```

## 📦 Zavisnosti

```bash
pip install -r requirements.txt
```

Potrebne biblioteke:
- Pandas - Rukovanje DataFrames
- NumPy - Numeričke operacije
- Scikit-learn - Transformacije i validacija
- ...

## ⚙️ Instalacija i Pokretanje

### 1. Kreiraj virtuelno okruženje
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Instaliraj zavisnosti
```bash
pip install -r requirements.txt
```

### 3. Pokreni preprocessing
```bash
python -m preprocessing
# ili
python preprocessing.py
```

## 🔄 Koraci Obrade

### 1. Validacija Podataka
- Provjera kolona i tipova podataka
- Identifikacija nedostajućih vrijednosti
- Detektovanje anomalija

### 2. Čišćenje Podataka
- ✅ Uklanjanje duplikata
- ✅ Obrada nedostajućih vrijednosti (NaN)
- ✅ Čišćenje numeričkih kolona (trim outliers)
- ✅ Čišćenje tekstualnih kolona

### 3. Normalizacija i Transformacija
- Skaliranje numeričkih vrijednosti
- Standardizacija
- Uklanjanje outliera IQR metodom za `price` i `area`

### 4. Feature Engineering

Kreiraju se nove vrijednosti:

| Novi Feature | Opis |
|-------------|------|
| `price_per_m2` | Cijena po kvadratnom metru |
| `building_age` | Starost zgrade |
| `floor_ratio` | Omjer sprata |
| `elevator` | Binarna vrijednost (0/1) |
| `terrace` | Binarna vrijednost (0/1) |
| `parking` | Binarna vrijednost (0/1) |
| City (one-hot) | One-hot encoding za grad |
| Municipality (one-hot) | One-hot encoding za opštinu |

### 5. Izlazni Dataset

Finalni obrađeni podaci se čuvaju u `processed_dataset.csv` u formatu spreman za trening modela.

## 📊 Inputi i Outputi

| Datoteka | Opis | Format |
|----------|------|--------|
| `dataset.csv` | Sirovinski podaci od scrapera | CSV |
| `processed_dataset.csv` | Obrađeni, spreman za ML | CSV |

## 🔗 Sljedeći Korak

Nakon što se podaci obrade, preidi na **ML Pipeline** fazu za trening modela.