# Predvidjanje cena nekretnina uz pomoc koriscenja vestacke inteligencije

Kompletan projekat za predvidjanje cena nekretnina uz pomoc machine learning modela. Projekat obuhvata sve faze od prikupljana raw podatak do njihove obrade i upotrebe

Projekat je organizovan u 4 glavne faze:

### 1. **Scrapper za nekretnine.rs**
Automatsko prikupljanje podataka sa veb-sajta nekretnine.rs 
- Ekstraktovanje informacija o nekretninama
- cuvanje podataka u CSV fajlu

### 2. **Validacija podataka i preprocessing**
Obrada i priprema podataka za machine learning modele
- Validacija integriteta podataka
- Patchovanje nedostataka, uklanajnej koppija islicmno
- Feature engineering
- Normalizacija podataka

### 3. **ML Pipeline** 
Treniranje, evaluacija i izbor najboljeg machine learning modela
- Testiranje vise algoritama
- Analiza i vizuelizacija podataka tj EDA
- Poredjenje performansi modela
- Izbor i cuvanje najboljeg modela

### 4. **Streamlit Aplikacija**
Interaktivna web aplikacija za predvidjanje cena nekretnina
- user friendly interfejs
- Prikaz predikcije u realnom vrmeenu
- Vizuelizacija rezultata




Svaki folder sadrži detaljnu `README.md` datoteku:

- [Scrapper README](1.%20Scrapper%20za%20nekretnine.rs/README.md)
- [Validacija README](2.%20Validacija%20podataka%20i%20preprocessing/README.md)
- [ML Pipeline README](3.%20ML%20pipeline%20za%20treniranje,%20evaluaciju%20i%20izbor%20najboljeg%20modela/README.md)
- [Streamlit App README](4.%20Streamlit%20app/README.md)



## Koriscene biblioteke

- **Prikupljanje podataka**: BeautifulSoup, Requests, Selenium
- **Obrada podataka**: Pandas, NumPy, Scikit-learn
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM
- **Web interfejs**: Streamlit
- **Analiza**: Jupyter Notebook, Matplotlib, Seaborn