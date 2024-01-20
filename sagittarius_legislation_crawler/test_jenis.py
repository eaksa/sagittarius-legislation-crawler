from typing import Generator

from pytest import fixture
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from sagittarius_legislation_crawler.get_jenis import Jenis, get_jenis


@fixture(scope="session")
def web_driver() -> Generator[WebDriver, None, None]:
    """Spawn a headless Chrome driver with Selenium."""

    # Set up Chrome web driver with automatic driver management
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")

    # Spawn webdriver
    driver = WebDriver(
        service=service,
        options=options
    )
    try:
        yield driver
    finally:
        try:
            driver.close()
        except:
            pass


@fixture(scope="module")
def jenis_256(web_driver: WebDriver) -> Generator[Jenis | None, None, None]:
    """Get the number of contents for jenis 256."""
    jenis = get_jenis(256, web_driver)
    try:
        yield jenis
    finally:
        web_driver.close()


def test_jenis_name(jenis_256: Jenis) -> None:
    assert jenis_256.name == "Peraturan Kepala Badan Informasi Geospasial"


def test_jenis_number_of_contents(jenis_256: Jenis) -> None:
    assert jenis_256.contents == 12
