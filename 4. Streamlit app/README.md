# 🌐 Streamlit Aplikacija - Predviđanje Cena Nekretnina

Interaktivna web aplikacija za predviđanje budućih cena nekretnina korišćenjem treniranog machine learning modela. Korisnici mogu da unesu karakteristike nekretnine i dobiju procijenjenu cijenu u realnom vremenu.

## 📋 Opis

Ova Streamlit aplikacija:
- Učitava prethodno trenirani ML model
- Omogućava korisniku da unese karakteristike nekretnine
- Pretvara unos u isti format kao treniranje
- Daje predikciju cijene u realnom vremenu
- Prikazuje vizuelne rezultate i analizu

## 🛠️ Arhitektura

```
├── app/
│   └── streamlit_app.py          # Glavna Streamlit aplikacija
├── src/
│   ├── __init__.py
│   ├── predict.py                # Logika predikcije
│   ├── input_schema.py           # Validacija unosa
│   └── utils.py                  # Pomoćne funkcije
├── data/
│   └── processed/
│       └── processed_dataset.csv # Referentni podaci
└── models/                       # Folder za modele (iz ML pipeline faze)
```

## 📦 Zavisnosti

```bash
pip install -r requirements.txt
```

Potrebne biblioteke:
- **Streamlit** - Web framework
- **Pandas & NumPy** - Rukovanje podacima
- **Scikit-learn** - ML modeli i transformacije
- **Joblib** - Učitavanje sačuvanih modela
- **Plotly** - Interaktivne vizuelizacije
- ...

## ⚙️ Instalacija i Pokretanje

### 1. Provjeri da li su podaci dostupni

Prije pokretanja aplikacije, osiguraj da su dostupni:
- `../3. ML pipeline.../models/best_model.pkl`
- `data/processed/processed_dataset.csv`

### 2. Kreiraj virtuelno okruženje
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instaliraj zavisnosti
```bash
pip install -r requirements.txt
```

### 4. Pokreni aplikaciju

**Opcija 1: Iz foldera Streamlit app**
```bash
streamlit run app/streamlit_app.py
```

**Opcija 2: Iz root direktorijuma projekta**
```bash
cd "4. Streamlit app"
streamlit run app/streamlit_app.py
```

Aplikacija će biti dostupna na `http://localhost:8501`

## 🎯 Funkcionalnosti

### Unos Parametara

Korisnik može unijeti sljedeće karakteristike:

| Parametar | Tip | Opis |
|-----------|-----|------|
| Grad | Select | Odabir gradu iz liste |
| Opština | Select | Odabir opštine |
| Vrsta Nekretnine | Select | Apartman, Kuća, Komercialni, itd. |
| Kvadratura (m²) | Numerička | Veličina nekretnine |
| Broj Soba | Numerička | Broj soba |
| Sprat | Numerička | Sprat nekretnine |
| Lift | Checkbox | Da li postoji lift |
| Terasa | Checkbox | Da li postoji terasa |
| Parking | Checkbox | Da li postoji parking |
| Starost Zgrade | Numerička | Starost u godinama |

### Predikcija Rezultata

Nakon unosa podataka, aplikacija:
1. ✅ Validira unos
2. ✅ Transformira u ML format
3. ✅ Prosljeđuje modelu
4. ✅ Prikazuje procijenjenu cijenu

### Vizuelizacija

- 📊 Grafički prikaz predikcije
- 📈 Historija predikcija (ako je aktivirano)
- 📉 Analiza uticaja parametara

## 🔗 Moduli

### `app/streamlit_app.py`
Glavna aplikacija sa Streamlit UI komponentama.

### `src/predict.py`
Logika učitavanja modela i generisanja predikcije.

### `src/input_schema.py`
Validacija i transformacija korisničkog unosa.

### `src/utils.py`
Pomoćne funkcije za preobradu podataka.

## 🚀 Primjer Korištenja

1. **Pokreni aplikaciju**
   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **U web interfejsu:**
   - Odaberi grad (npr. Beograd)
   - Odaberi opštinu (npr. Voždovac)
   - Unesi kvadraturu (npr. 75 m²)
   - Izaberi ostale parametre
   - Klikni "Predvidi Cijenu"

3. **Rezultat:** Aplikacija prikazuje procijenjenu cijenu nekretnine

## 🎨 Prilagođavanje

Za prilagođavanje UI-a, izmijeni `streamlit_app.py`:

```python
# Primjer: Dodaj novi parametar
diameter = st.slider("Novi Parametar", min_value=0, max_value=100)
```

## 📞 Deployment

Za deployment na cloud servisu (npr. Streamlit Cloud):

```bash
# Pripremi requirements.txt
pip freeze > requirements.txt

# Dodaj na GitHub
git add .
git commit -m "Deploy ready"
git push
```

Zatim u Streamlit Cloud interfejsu odaberi GitHub repo i deploy.

## 🔗 Povezane Komponente

- **ML Model**: `3. ML pipeline...`
- **Obrada Podataka**: `2. Validacija podataka i preprocessing`
- **Sirovi Podaci**: `1. Scrapper za nekretnine.rs`

## 💡 Savjeti

- Čuva unose lokalno za brže ponavljajuće predikcije
- Periodički ažuriraj model sa novim podacima
- Testiraj predikcije sa poznatim primjerima
- Prilagodi UI prema povratnoj informaciji korisnika

