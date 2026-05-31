# Streamlit App

Aplikacija ucitava `models/best_model.pkl`, prima korisnicki unos( godinu/opstinu i slicno), pretvara ga u isti feature format koji model ocekuje i prikazuje procenjenu cenu nekretnine



## Instalacija i pokretanje


python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt


Iz ovog foldera 

```bash
.\.venv\Scripts\streamlit.exe run app/streamlit_app.py
```

Root projekta ako windows odbija da pokrne iz prethodnog

```bash
..\..\.venv\Scripts\streamlit.exe run app/streamlit_app.py
```

