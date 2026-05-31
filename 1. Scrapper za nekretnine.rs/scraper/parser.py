import json
import logging
import re
from typing import Any, Optional

from bs4 import BeautifulSoup

from .models import PropertyListing

logger = logging.getLogger(__name__)


ROOM_WORDS = {
    "garsonjera": 0.5,
    "jednosoban": 1.0,
    "jednoiposoban": 1.5,
    "dvosoban": 2.0,
    "dvoiposoban": 2.5,
    "trosoban": 3.0,
    "troiposoban": 3.5,
    "\u010detvorosoban": 4.0,
    "cetvorosoban": 4.0,
    "petosoban": 5.0,
}


def _clean_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _to_float(value: str | None) -> Optional[float]:
    if not value:
        return None

    normalized = value.replace("\xa0", " ")
    match = re.search(r"\d+(?:[\s.]\d{3})*(?:[,.]\d+)?|\d+(?:[,.]\d+)?", normalized)
    if not match:
        return None

    number = match.group(0).replace(" ", "")
    if "," in number and "." in number:
        number = number.replace(".", "").replace(",", ".")
    elif "," in number:
        number = number.replace(",", ".")
    elif re.search(r"\.\d{3}(?:\D|$)", number):
        number = number.replace(".", "")

    try:
        return float(number)
    except ValueError:
        return None


def _field_after_label(soup: BeautifulSoup, labels: tuple[str, ...]) -> Optional[str]:
    label_pattern = re.compile("|".join(re.escape(label) for label in labels), re.IGNORECASE)

    for element in soup.find_all(string=label_pattern):
        parent = element.parent
        if parent is None:
            continue

        label_text = _clean_text(element)
        parent_text = _clean_text(parent.get_text(" ", strip=True))
        value = parent_text.replace(label_text, "", 1).strip(" :")
        if value and value.lower() not in {label.lower() for label in labels}:
            return value

        sibling = parent.find_next_sibling()
        if sibling:
            sibling_text = _clean_text(sibling.get_text(" ", strip=True))
            if sibling_text:
                return sibling_text

        container = parent.parent
        if container and container.name not in {"body", "html"}:
            container_text = _clean_text(container.get_text(" ", strip=True))
            value = container_text.replace(label_text, "", 1).strip(" :")
            if value and value.lower() not in {label.lower() for label in labels}:
                return value

    return None


def _json_ld_objects(soup: BeautifulSoup) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            objects.append(data)
        elif isinstance(data, list):
            objects.extend(item for item in data if isinstance(item, dict))
    return objects


def _next_data(soup: BeautifulSoup) -> Optional[dict[str, Any]]:
    script = soup.select_one("#__NEXT_DATA__")
    if script is None or not script.string:
        return None

    try:
        data = json.loads(script.string)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _parse_floor_value(value: Any) -> Optional[int]:
    if value is None:
        return None

    text = str(value)
    if re.search(r"\b(prizemlje|pr)\b", text, re.IGNORECASE):
        return 0
    if re.search(r"\b(suteren|podrum)\b", text, re.IGNORECASE):
        return -1

    match = re.search(r"(?<!\d)(\d{1,2})(?!\d)", text)
    return int(match.group(1)) if match else None


def _parse_next_detail_listing(soup: BeautifulSoup, url: str) -> Optional[PropertyListing]:
    data = _next_data(soup)
    if not data:
        return None

    detail_data = data.get("props", {}).get("pageProps", {}).get("detailData")
    if not isinstance(detail_data, dict):
        return None

    real_estate = detail_data.get("realEstate")
    if not isinstance(real_estate, dict):
        return None

    properties = real_estate.get("properties") or []
    property_data = properties[0] if properties and isinstance(properties[0], dict) else {}
    location = property_data.get("location") or {}
    floor_data = property_data.get("floor") or {}

    primary_features = property_data.get("primaryFeatures") or []
    feature_codes = {
        str(feature.get("codeName", "")).lower()
        for feature in primary_features
        if isinstance(feature, dict)
    }
    feature_names = {
        str(feature.get("name", "")).lower()
        for feature in primary_features
        if isinstance(feature, dict)
    }

    price_data = real_estate.get("price") or property_data.get("price") or {}
    rooms = property_data.get("roomsValue") or property_data.get("rooms")
    if isinstance(rooms, str) and rooms.endswith("+"):
        rooms = rooms.rstrip("+")

    return PropertyListing(
        title=real_estate.get("title") or property_data.get("caption"),
        price=_to_float(str(price_data.get("value") or "")),
        area=_to_float(str(property_data.get("surfaceValue") or property_data.get("surface") or "")),
        rooms=_to_float(str(rooms or "")),
        city=location.get("city"),
        municipality=location.get("macrozone") or location.get("microzone"),
        floor=_parse_floor_value(floor_data.get("floorOnlyValue") or floor_data.get("value")),
        total_floors=_parse_floor_value(property_data.get("floors")),
        building_year=int(property_data["buildingYear"])
        if property_data.get("buildingYear")
        else None,
        elevator=bool(property_data.get("elevator")),
        terrace=bool({"terrace", "balcony", "loggia"} & feature_codes)
        or bool({"terasa", "balkon", "lodja", "lo\u0111a"} & feature_names),
        parking=bool(property_data.get("garage"))
        or bool({"garage", "parking_space", "parking"} & feature_codes),
        url=url,
    )


def parse_price(soup: BeautifulSoup) -> Optional[float]:
    for data in _json_ld_objects(soup):
        offers = data.get("offers")
        if isinstance(offers, dict):
            price = _to_float(str(offers.get("price") or ""))
            if price:
                return price

    candidates = [
        '[class*="price"]',
        '[class*="Price"]',
        '[data-test*="price"]',
    ]
    for selector in candidates:
        for element in soup.select(selector):
            text = _clean_text(element.get_text(" ", strip=True))
            if "\u20ac" in text or "eur" in text.lower():
                price = _to_float(text)
                if price:
                    return price

    return _to_float(_field_after_label(soup, ("Cena", "Price")))


def parse_area(soup: BeautifulSoup) -> Optional[float]:
    value = _field_after_label(soup, ("Kvadratura", "Povr\u0161ina", "Povrsina", "Area"))
    if value:
        area = _to_float(value)
        if area:
            return area

    text = _clean_text(soup.get_text(" ", strip=True))
    match = re.search(r"(\d+(?:[,.]\d+)?)\s*(?:m\u00b2|m2|m\^2)", text, re.IGNORECASE)
    return _to_float(match.group(1)) if match else None


def parse_rooms(soup: BeautifulSoup) -> Optional[float]:
    text = _clean_text(soup.get_text(" ", strip=True)).lower()

    room_value = _field_after_label(soup, ("Ukupan broj soba", "Broj soba", "Sobe"))
    if room_value:
        parsed = _to_float(room_value)
        if parsed is not None:
            return parsed

    match = re.search(r"\b([0-9](?:[,.][05])?)\s*(?:soba|soban|sobni)\b", text)
    if match:
        parsed = _to_float(match.group(1))
        if parsed is not None and 0 < parsed < 20:
            return parsed

    for word, value in ROOM_WORDS.items():
        if word in text:
            return value

    return None


def parse_location(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
    location = _field_after_label(soup, ("Lokacija", "Mesto", "Adresa"))
    if not location:
        breadcrumbs = [
            _clean_text(item.get_text(" ", strip=True))
            for item in soup.select(".breadcrumb a, .breadcrumbs a, nav a")
        ]
        location = ", ".join(part for part in breadcrumbs if part)

    if not location:
        text = _clean_text(soup.get_text(" ", strip=True))
        match = re.search(r"([^,]+),\s*([^,]+),\s*Srbija", text)
        location = match.group(0) if match else ""

    parts = [part.strip() for part in location.split(",") if part.strip()]
    city = None
    municipality = None

    for part in parts:
        if part.lower() in {"beograd", "novi sad", "nis", "ni\u0161", "kragujevac"}:
            city = part
            break

    if parts:
        municipality = parts[0]

    return city, municipality


def parse_floor(soup: BeautifulSoup) -> tuple[Optional[int], Optional[int]]:
    title_element = soup.select_one("h1") or soup.select_one("h2") or soup.select_one("title")
    title = _clean_text(title_element.get_text(" ", strip=True) if title_element else None)
    floor_text = _field_after_label(soup, ("Spratnost", "Sprat", "Floor")) or title

    if re.search(r"\b(prizemlje|pr)\b", floor_text, re.IGNORECASE):
        floor = 0
    elif re.search(r"\b(suteren|podrum)\b", floor_text, re.IGNORECASE):
        floor = -1
    else:
        match = re.search(r"(?<!\d)(\d{1,2})\s*/\s*(\d{1,2})(?!\d)", floor_text)
        if match:
            return int(match.group(1)), int(match.group(2))

        match = re.search(r"(?<!\d)(\d{1,2})\s*(?:\.|sprat|sp\b)", floor_text, re.IGNORECASE)
        floor = int(match.group(1)) if match else None

    total_match = re.search(r"/\s*(\d{1,2})(?!\d)", floor_text)
    total_floors = int(total_match.group(1)) if total_match else None
    return floor, total_floors


def parse_building_year(soup: BeautifulSoup) -> Optional[int]:
    year_text = _field_after_label(soup, ("Godina izgradnje", "Izgra\u0111eno", "Izgradnja"))
    if not year_text:
        return None

    match = re.search(r"\b(19\d{2}|20\d{2})\b", year_text)
    return int(match.group(1)) if match else None


def parse_features(soup: BeautifulSoup) -> dict[str, bool]:
    text = _clean_text(soup.get_text(" ", strip=True)).lower()
    return {
        "elevator": any(word in text for word in ("lift", "elevator")),
        "terrace": any(word in text for word in ("terasa", "balkon", "lo\u0111a", "lodja")),
        "parking": any(word in text for word in ("parking", "gara\u017ea", "garaza", "gara\u017eno")),
    }


def parse_listing(html: str, url: str) -> PropertyListing:
    soup = BeautifulSoup(html, "html.parser")

    next_listing = _parse_next_detail_listing(soup, url)
    if next_listing is not None:
        return next_listing

    title_element = soup.select_one("h1") or soup.select_one("h2") or soup.select_one("title")
    title = _clean_text(title_element.get_text(" ", strip=True) if title_element else None)

    city, municipality = parse_location(soup)
    floor, total_floors = parse_floor(soup)
    features = parse_features(soup)

    return PropertyListing(
        title=title or None,
        price=parse_price(soup),
        area=parse_area(soup),
        rooms=parse_rooms(soup),
        city=city,
        municipality=municipality,
        floor=floor,
        total_floors=total_floors,
        building_year=parse_building_year(soup),
        elevator=features["elevator"],
        terrace=features["terrace"],
        parking=features["parking"],
        url=url,
    )
