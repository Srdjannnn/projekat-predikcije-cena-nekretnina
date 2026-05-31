# ML treniranje

Ovim korakom se radi ML trening  projekta za predikciju cena nekretnina.

Koristi se `data/processed/processed_dataset.csv` ( koji je obradjen prethodnim korakom ), trenira tri regresiona modela, evaluira ih, i na kraju bira najbolji model i sacuva ga u folderu ; `models/best_model.pkl`


## Instalacija i pokretanje


python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\.venv\Scripts\python.exe -m src.train_model

Funkcije ovog Pipeline:

- ucitavanej prethodno obradjenog dataseta
- split na X/y
- train/test split 80/20
- treniranje `LinearRegression`, `RandomForestRegressor`, `GradientBoostingRegressor`
- evaluaciju metrikama MAE, RMSE i R2
- izbor najboljeg modela po RMSE, uz R2 kao tie-breaker
- cuvan najbolji modela u `models/best_model.pkl`
- cuvanje poredbenih metrika u `models/model_comparison.csv`
