import logging
import json
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Iterable
from urllib.parse import urljoin
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import (
    MAX_PAGES,
    MAX_RETRIES,
    NEKRETNINE_START_URL,
    OUTPUT_FILE,
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    USER_AGENT,
)
from .models import PropertyListing
from .parser import parse_listing
from .save_data import save_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    def __init__(
        self,
        start_url: str,
        max_pages: int = MAX_PAGES,
        request_delay: float = REQUEST_DELAY,
        timeout: int = REQUEST_TIMEOUT,
        output_file=OUTPUT_FILE,
    ) -> None:
        self.start_url = start_url
        self.max_pages = max_pages
        self.request_delay = request_delay
        self.timeout = timeout
        self.output_file = output_file
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

        retry = Retry(
            total=MAX_RETRIES,
            connect=MAX_RETRIES,
            read=MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def fetch_page(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        time.sleep(self.request_delay)
        return response.text

    @abstractmethod
    def get_listing_urls(self) -> list[str]:
        """Return detail-page URLs for listings."""

    @abstractmethod
    def scrape_listing(self, url: str) -> PropertyListing | None:
        """Scrape one listing detail page."""

    def scrape_all(self) -> list[PropertyListing]:
        logger.info("Pocetak scrape procesa: %s", self.start_url)
        listing_urls = self.get_listing_urls()
        logger.info("Broj pronadjenih URL-ova oglasa: %s", len(listing_urls))

        unique_listings: OrderedDict[str, PropertyListing] = OrderedDict()
        for index, url in enumerate(listing_urls, start=1):
            try:
                listing = self.scrape_listing(url)
            except Exception as exc:
                logger.exception("Greska pri parsiranju oglasa %s: %s", url, exc)
                continue

            if listing is None:
                continue
            if not listing.is_valid():
                logger.info("Preskocen nevalidan oglas: %s", url)
                continue

            unique_listings[listing.url] = listing
            if index % 50 == 0:
                logger.info("Obradjeno %s/%s oglasa", index, len(listing_urls))

        listings = list(unique_listings.values())
        save_to_csv(listings, self.output_file)
        logger.info("Broj uspesno sacuvanih oglasa: %s", len(listings))
        return listings


class NekretnineRsScraper(BaseScraper):
    def __init__(self, start_url: str = NEKRETNINE_START_URL, **kwargs) -> None:
        super().__init__(start_url=start_url, **kwargs)
        self.base_url = "https://www.nekretnine.rs"

    def _page_url(self, page_number: int) -> str:
        if page_number <= 1:
            return self.start_url

        normalized = self.start_url.rstrip("/") + "/"
        separator = "&" if "?" in normalized else "?"
        return f"{normalized}{separator}{urlencode({'pag': page_number})}"

    def _extract_listing_links(self, html: str) -> Iterable[str]:
        soup = BeautifulSoup(html, "html.parser")

        yield from self._extract_listing_links_from_next_data(soup)

        for anchor in soup.select("h2 a[href], h3 a[href], article a[href], .offer-title a[href]"):
            href = anchor.get("href")
            if not href:
                continue

            absolute_url = urljoin(self.base_url, href)
            if self._is_listing_url(absolute_url):
                yield absolute_url

    def _extract_listing_links_from_next_data(self, soup: BeautifulSoup) -> Iterable[str]:
        script = soup.select_one("#__NEXT_DATA__")
        if script is None or not script.string:
            return

        try:
            data = json.loads(script.string)
        except json.JSONDecodeError:
            return

        queries = (
            data.get("props", {})
            .get("pageProps", {})
            .get("dehydratedState", {})
            .get("queries", [])
        )

        for query in queries:
            query_data = query.get("state", {}).get("data")
            if not isinstance(query_data, dict):
                continue

            for item in query_data.get("results", []):
                seo = item.get("seo", {}) if isinstance(item, dict) else {}
                url = seo.get("url")
                if isinstance(url, str) and self._is_listing_url(url):
                    yield url

    def _is_listing_url(self, url: str) -> bool:
        skipped_fragments = (
            "/lista/",
            "/pretraga/",
            "/agencije/",
            "/investitori/",
            "/magazin/",
            "/novogradnja-projekti/",
        )
        return (
            url.startswith(self.base_url)
            and ("/oglasi/" in url or "/stambeni-objekti/stanovi/" in url)
            and not any(fragment in url for fragment in skipped_fragments)
        )

    def get_listing_urls(self) -> list[str]:
        urls: OrderedDict[str, None] = OrderedDict()

        for page_number in range(1, self.max_pages + 1):
            page_url = self._page_url(page_number)
            try:
                html = self.fetch_page(page_url)
            except requests.RequestException as exc:
                logger.warning("Ne mogu da preuzmem listu oglasa %s: %s", page_url, exc)
                break

            page_links = list(self._extract_listing_links(html))
            logger.info("Strana %s: pronadjeno %s oglasa", page_number, len(page_links))
            if not page_links:
                break

            for listing_url in page_links:
                urls[listing_url] = None

        return list(urls.keys())

    def scrape_listing(self, url: str) -> PropertyListing | None:
        html = self.fetch_page(url)
        if "oglas vi\u0161e nije aktivan" in html.lower():
            logger.info("Oglas vise nije aktivan: %s", url)
            return None
        return parse_listing(html, url)


if __name__ == "__main__":
    scraper = NekretnineRsScraper()
    scraper.scrape_all()
