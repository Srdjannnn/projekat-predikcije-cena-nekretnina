from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class PropertyListing:
    title: Optional[str]
    price: Optional[float]
    area: Optional[float]
    rooms: Optional[float]
    city: Optional[str]
    municipality: Optional[str]
    floor: Optional[int]
    total_floors: Optional[int]
    building_year: Optional[int]
    elevator: bool
    terrace: bool
    parking: bool
    url: str

    def is_valid(self) -> bool:
        return (
            self.price is not None
            and self.area is not None
            and self.price > 0
            and self.area > 0
        )

    def to_dict(self) -> dict:
        return asdict(self)

