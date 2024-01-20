from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


def get_jenis(jenis_id: int, browser: WebDriver) -> dict[str, str | int] | None:
    url = f"https://peraturan.bpk.go.id/Search?jenis={jenis_id}"
    browser.get(url)

    try:
        name = browser.find_element(
            By.CSS_SELECTOR, 
            "div.g-8:nth-child(3) > div:nth-child(1) > span > span > span > ul > li > span"
        ).text

        contents = browser.find_element(
            By.CSS_SELECTOR, 
            "p.text-danger"
        ).text.split()[1].replace(".", "")
        return {"name": name, "contents": int(contents)}
    except:
        return None



if __name__ == "__main__":
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
    result = {}
    for i in range(1, 300):
        result[str(i)] = get_jenis(i, driver)
    # save to json
    import json

    with open("jenis.json", "w") as f:
        json.dump(result, f, indent=4)
