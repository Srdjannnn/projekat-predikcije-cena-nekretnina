from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

REQUEST_DELAY = 1.5
MAX_PAGES = 50
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)

OUTPUT_FILE = BASE_DIR / "data" / "raw" / "dataset.csv"

NEKRETNINE_START_URL = "https://www.nekretnine.rs/prodaja-stanova/beograd/"
