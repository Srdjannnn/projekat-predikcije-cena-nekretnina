
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyInput:
    """Validated user input for a single real-estate prediction."""

    area: float
    rooms: int
    city: str
    municipality: str
    floor: int
    total_floors: int
    building_year: int
    elevator: bool
    terrace: bool
    parking: bool


CITY_OPTIONS = ["Beograd"]

MUNICIPALITY_OPTIONS = [
    "Barajevo",
    "Grocka",
    "Mladenovac",
    "Novi Beograd",
    "Obrenovac",
    "Palilula",
    "Rakovica",
    "Savski Venac",
    "Sopot",
    "Stari Grad",
    "Sur\u010din",
    "Vo\u017edovac",
    "Vra\u010dar",
    "Zemun",
    "Zvezdara",
    "\u010cukarica",
]

