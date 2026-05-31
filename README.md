# Predviđanje Cena Nekretnina pomoću Vještačke Inteligencije 🏠📈

Kompletan projekat za predviđanje budućih cena nekretnina koristeći machine learning modele. Projekat obuhvata sve faze od prikupljanja podataka do razvoja web aplikacije.

## 📋 Pregled Projekta

Projekat je organizovan u četiri glavne faze:

### 1. **Scrapper za nekretnine.rs** 🕷️
Automatsko prikupljanje podataka sa veb-sajta nekretnine.rs korišćenjem web scraper tehnologije.
- Ekstraktovanje informacija o nekretninama
- Čuvanje podataka u strukturiranom formatu (CSV)
- Konfigurabilne postavke za skreping

**Folder:** `1. Scrapper za nekretnine.rs/`

### 2. **Validacija podataka i preprocessing** 🔍
Čišćenje i priprema podataka za machine learning modele.
- Validacija integritet podataka
- Tratiranje nedostajućih vrijednosti
- Feature engineering
- Normalizacija podataka

**Folder:** `2. Validacija podataka i preprocessing/`

### 3. **ML Pipeline** 🤖
Treniranje, evaluacija i izbor najboljeg machine learning modela.
- Testiranje više algoritama
- Analiza i vizuelizacija podataka (EDA)
- Poređenje performansi modela
- Izbor i skladištenje najbolje modela

**Folder:** `3. ML pipeline za treniranje, evaluaciju i izbor najboljeg modela/`

### 4. **Streamlit Aplikacija** 🌐
Interaktivna web aplikacija za predviđanje cena nekretnina.
- Korisničko okruženje (UI)
- Realnom vremenu predikcija
- Vizuelizacija rezultata

**Folder:** `4. Streamlit app/`

## 🚀 Brzi Start

### Preduslov
- Python 3.8+
- pip ili conda

### Instalacija

1. **Kloniranje repozitorijuma**
```bash
git clone https://github.com/vas-github-username/nekretnine-price-prediction.git
cd "Vestacka Inteligencija projekat aproksimacije buducih cena nekretnina"
```

2. **Kreiraj virtuelno okruženje**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instaliraj zavisnosti**
```bash
# Za sve dijelove
pip install -r requirements.txt

# Ili za specifičan dio (npr. Streamlit aplikacija)
cd "4. Streamlit app"
pip install -r requirements.txt
```

## 📖 Detaljne Upustvke po Folderima

Svaki folder sadrži detaljnu `README.md` datoteku:

- [Scrapper README](1.%20Scrapper%20za%20nekretnine.rs/README.md)
- [Validacija README](2.%20Validacija%20podataka%20i%20preprocessing/README.md)
- [ML Pipeline README](3.%20ML%20pipeline%20za%20treniranje,%20evaluaciju%20i%20izbor%20najboljeg%20modela/README.md)
- [Streamlit App README](4.%20Streamlit%20app/README.md)

## 🔄 Redoslijed Izvršavanja

1. **Prikupljanje podataka**: `1. Scrapper za nekretnine.rs`
2. **Obrada podataka**: `2. Validacija podataka i preprocessing`
3. **Treniranje modela**: `3. ML pipeline za treniranje, evaluaciju i izbor najbolje modela`
4. **Pokretanje aplikacije**: `4. Streamlit app`

## 🌳 Struktura Podataka

```
data/
├── dataset.csv                    # Originalni skrapirani podaci
├── processed_dataset.csv          # Obrađeni podaci
├── model_comparison.csv           # Rezultati poređenja modela
└── streamlit_processed_dataset.csv # Podaci za Streamlit

models/
├── model_comparison.csv           # Performanse različitih modela
└── [trained_models]              # Sačuvani treniran modeli
```

## 📊 Korišćene Tehnologije

- **Prikupljanje podataka**: BeautifulSoup, Requests, Selenium
- **Obrada podataka**: Pandas, NumPy, Scikit-learn
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM
- **Web okruženje**: Streamlit
- **Analiza**: Jupyter Notebook, Matplotlib, Seaborn

## 📝 Licence

Ovaj projekat je nastao kao dio nastavnog predmeta.

## 👨‍💻 Autor

[Vaše Ime/GitHub Profil]

## 📧 Kontakt

Za pitanja ili sugestije, slobodno otvorite GitHub issue.

---

**Napomena**: Ovo je obrazovni projekat. Preporuka je da poštujete Terms of Service web-sajta pri skrapiranju podataka.
