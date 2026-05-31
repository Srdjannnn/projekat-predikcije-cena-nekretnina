# 🤖 ML Pipeline - Treniranje, Evaluacija i Izbor Modela

Kompletan pipeline za treniranje različitih machine learning modela, njihovu evaluaciju i izbor najboljeg modela za predviđanje cena nekretnina.

## 📋 Opis

Ovaj modul:
1. Učitava prethodno obrađene podatke
2. Trenira više regresionih modela
3. Evaluira performanse svake modela
4. Bira i čuva najbolji model
5. Generiše izvještaj o poređenju modela

## 🛠️ Arhitektura

```
├── src/
│   ├── __init__.py              # Inicijalizacija
│   ├── train_model.py           # Glavna obrada treniranja
│   ├── evaluate.py              # Evaluacijske metrike
│   ├── model_selection.py       # Izbor najboljeg modela
│   └── save_model.py            # Čuvanje modela
├── notebooks/
│   └── eda_and_training.ipynb   # EDA i vizuelizacija
├── data/
│   └── processed/
│       └── processed_dataset.csv # Ulazni obrađeni podaci
└── models/
    ├── best_model.pkl           # Sačuvani najbolji model
    └── model_comparison.csv     # Rezultati evaluacije
```

## 📦 Zavisnosti

```bash
pip install -r requirements.txt
```

Potrebne biblioteke:
- Scikit-learn - ML modeli i metrike
- Pandas & NumPy - Rukovanje podacima
- Matplotlib & Seaborn - Vizuelizacija
- Joblib - Čuvanje modela
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

### 3. Pokreni treniranje
```bash
# Direktno pokretanje
python -m src.train_model

# Ili iz root direktorijuma
python -m "3. ML pipeline...".src.train_model
```

## 📊 Koraci Procesa

### 1. Priprema Podataka
- Učitavanje `processed_dataset.csv`
- Odvajanje features (X) i target vrijednosti (y)
- Train/Test split: **80% treniranje, 20% testiranje**

### 2. Treniranje Modela

Tri regresiona modela se treniraju:

| Model | Opis | Parametri |
|-------|------|-----------|
| **Linear Regression** | Linearna regresija | Default |
| **Random Forest** | Ensemble metoda sa odlukama | n_estimators=100 |
| **Gradient Boosting** | Sekvencijalna ensemble metoda | n_estimators=100 |

### 3. Evaluacija Performansi

Metrike za evaluaciju:

| Metrika | Opis |
|---------|------|
| **MAE** | Mean Absolute Error - Prosječna apsolutna greška |
| **RMSE** | Root Mean Squared Error - Korijen srednje kvadratne greške |
| **R²** | R-squared - Koeficijent determinacije (0-1) |

### 4. Izbor Najboljeg Modela

Kriterij izbora:
1. **Primarni**: Najmanja RMSE vrijednost
2. **Tie-breaker**: Najveća R² vrijednost
3. **Rezultat**: Sačuvava se u `models/best_model.pkl`

### 5. Izvještaji

Poređenje modela se čuva u `models/model_comparison.csv`:
```csv
model,mae,rmse,r2,train_time
LinearRegression,25000,35000,0.85,0.01
RandomForest,20000,30000,0.90,0.05
GradientBoosting,18000,28000,0.92,0.08
```

## 📈 EDA i Vizuelizacija

Jupyter Notebook `notebooks/eda_and_training.ipynb` sadrži:
- Eksplorativnu analizu podataka (EDA)
- Vizuelizaciju distribucije podataka
- Feature importance analizu
- Predviđanja vs. stvarnih vrijednosti

### Pokretanje Notebooka
```bash
jupyter notebook notebooks/eda_and_training.ipynb
```

## 🔗 Sljedeći Korak

Nakon što se model trenira i evaluira, preidi na **Streamlit Aplikacija** za predikcije u realnom vremenu.
