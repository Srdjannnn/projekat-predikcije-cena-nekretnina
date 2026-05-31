"""Streamlit web app for real-estate price prediction."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.input_schema import CITY_OPTIONS, MUNICIPALITY_OPTIONS, PropertyInput
from src.predict import load_model, predict_price
from src.utils import format_euro, get_feature_importance, load_processed_dataset

MODEL_PATH = PROJECT_ROOT / "models" / "best_model.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_dataset.csv"


st.set_page_config(
    page_title="Predikcija cena nekretnina",
    layout="wide",
)


@st.cache_resource
def cached_model() -> object:
    """Load the model once per Streamlit session."""
    return load_model(MODEL_PATH)


@st.cache_data
def cached_dataset() -> pd.DataFrame:
    """Load processed data once per Streamlit session."""
    return load_processed_dataset(DATA_PATH)


def reset_form() -> None:
    """Reset key form values to sensible defaults."""
    defaults = {
        "area": 55.0,
        "rooms": 2,
        "city": CITY_OPTIONS[0],
        "municipality": "Novi Beograd",
        "floor": 2,
        "total_floors": 5,
        "building_year": 2005,
        "elevator": True,
        "terrace": True,
        "parking": False,
    }
    for key, value in defaults.items():
        st.session_state[key] = value


def main() -> None:
    """Render the Streamlit app."""
    model = cached_model()
    dataset = cached_dataset()

    st.title("Predikcija cena nekretnina")
    st.caption("Jednostavan ML sistem: unos podataka -> model -> procenjena cena")

    with st.sidebar:
        st.header("O projektu")
        st.write(
            "Aplikacija koristi model treniran oglasima sa nekretnine.rs, "
            "nakon validacije podataka, feature engineeringa i uporedjivanja modela."
        )
        st.write("Model daje aproksimaciju cene")
        st.divider()
        st.write(f"Model: `{type(model).__name__}`")
        st.write(f"Broj redova u processed dataset-u: `{len(dataset)}`")

    left, right = st.columns(2)

    with left:
        area = st.number_input(
            "Kvadratura",
            min_value=10.0,
            max_value=500.0,
            value=st.session_state.get("area", 55.0),
            step=1.0,
            key="area",
        )
        rooms = st.number_input(
            "Broj soba",
            min_value=1,
            max_value=10,
            value=st.session_state.get("rooms", 2),
            step=1,
            key="rooms",
        )
        city = st.selectbox(
            "Grad",
            CITY_OPTIONS,
            index=CITY_OPTIONS.index(st.session_state.get("city", CITY_OPTIONS[0])),
            key="city",
        )
        municipality = st.selectbox(
            "Opstina",
            MUNICIPALITY_OPTIONS,
            index=MUNICIPALITY_OPTIONS.index(
                st.session_state.get("municipality", "Novi Beograd")
            ),
            key="municipality",
        )

    with right:
        floor = st.number_input(
            "Sprat",
            min_value=0,
            max_value=50,
            value=st.session_state.get("floor", 2),
            step=1,
            key="floor",
        )
        total_floors = st.number_input(
            "Ukupno spratova",
            min_value=1,
            max_value=60,
            value=st.session_state.get("total_floors", 5),
            step=1,
            key="total_floors",
        )
        building_year = st.number_input(
            "Godina gradnje",
            min_value=1900,
            max_value=2035,
            value=st.session_state.get("building_year", 2005),
            step=1,
            key="building_year",
        )
        c1, c2, c3 = st.columns(3)
        elevator = c1.checkbox("Lift", value=st.session_state.get("elevator", True), key="elevator")
        terrace = c2.checkbox("Terasa", value=st.session_state.get("terrace", True), key="terrace")
        parking = c3.checkbox("Parking", value=st.session_state.get("parking", False), key="parking")

    actions_left, actions_right = st.columns([1, 1])
    predict_clicked = actions_left.button("Predvidi cenu", type="primary", use_container_width=True)
    actions_right.button("Reset form", use_container_width=True, on_click=reset_form)

    if predict_clicked:
        user_input = PropertyInput(
            area=area,
            rooms=rooms,
            city=city,
            municipality=municipality,
            floor=floor,
            total_floors=total_floors,
            building_year=building_year,
            elevator=elevator,
            terrace=terrace,
            parking=parking,
        )
        prediction = predict_price(user_input, MODEL_PATH)
        st.markdown(
            f"""
            <div style="font-size: 2.25rem; font-weight: 700; margin: 1rem 0;">
                Procenjena cena: {format_euro(prediction)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    chart_col, importance_col = st.columns(2)

    with chart_col:
        st.subheader("Odnos kvadrature i cene")
        st.scatter_chart(dataset[["area", "price"]], x="area", y="price")

    with importance_col:
        st.subheader("Najvaxniji featurei")
        importance = get_feature_importance(model).head(10)
        if importance.empty:
            st.info("Ovaj model ne izlaze feature importance.")
        else:
            st.bar_chart(importance.set_index("feature"))


if __name__ == "__main__":
    main()
