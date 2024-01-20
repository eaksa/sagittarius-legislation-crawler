from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def crawl_bpk_perbup(
    year: int,
    jenis: int,
    entitas: str,
    browser: WebDriver,
    p_: int = 1
) -> list[str]:
    """Recursively crawls the BPK website for legislation page links, through
    its search functionality.

    Args:
        year: The year of the legislation.
        jenis: The type of legislation.
        browser: The browser to use.
    """
    url = (
        f"https://peraturan.bpk.go.id/Search?"
        f"tahun={year}"
        f"&entitas={entitas}"
        f"&jenis={jenis}"
        f"&p={p_}"
    )
    links = get_page_links(url, browser)
    return (
        links
        if len(links) == 0
        else links + crawl_bpk_perbup(year, jenis, entitas, browser, p_ + 1)
    )


def get_page_links(url: str, browser: WebDriver) -> list[str]:
    """Get the links to legislation on a search page.

    Args:
        url: The URL of the search page.
        browser: The browser to use.
    """
    # Download search page
    browser.get(url)

    # Get links
    link_selector = (
        "div.row "
        "> div:nth-child(1) "
        "> div:nth-child(1) "
        "> div:nth-child(1) "
        "> div:nth-child(2) "
        "> a:nth-child(2)"
    )
    link_elements = browser.find_elements(
        By.CSS_SELECTOR,
        link_selector
    )
    return [
        link_element.get_attribute("href") or ""
        for link_element in link_elements
    ]

if __name__ == "__main__":
    import json

    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.webdriver import WebDriver
    from webdriver_manager.chrome import ChromeDriverManager

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

    # Open JSON
    with open("jenis.json", "r") as f:
        jenis_json = json.load(f)

    with open("locales.json", "r") as f:
        locales_json = json.load(f)


    result = {}

    j = 23
    name = jenis_json[str(j)]["name"]
    # if jenis_json[str(j)]["contents"] == 0:
    #     continue
    result[name] = {}

    entitas = list(locales_json)

    for n in range(0, 210):
        e = entitas[n]
        for year in range(1945, 2024):
            try:
                result[name][year] = crawl_bpk_perbup(year, j, e, driver)
            except:
                driver = WebDriver(
                    service=service,
                    options=options
                )
                result[name][year] = crawl_bpk_perbup(year, j, e, driver)

    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)
