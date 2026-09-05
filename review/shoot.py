"""
Selenium screenshot script for reviewing the Heaven Furniture Mart landing page.

Loads index.html in headless Chrome (falls back to Edge) and captures:
  - Desktop full-page  (1440 wide)
  - Desktop viewport   (1440 x 900, above-the-fold)
  - Mobile full-page   (390 wide, iPhone-ish)

Screenshots are saved into review/shots/.

Usage:
    python review/shoot.py

Requires: pip install selenium   (Selenium 4 auto-manages the driver)
"""

import time
import base64
import pathlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
INDEX = PROJECT / "index.html"
OUT = HERE / "shots"
OUT.mkdir(parents=True, exist_ok=True)

URL = INDEX.as_uri()  # file:///D:/Level%201/... correctly encoded


def make_driver():
    """Try Chrome first, then Edge. Both headless."""
    try:
        opts = ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--hide-scrollbars")
        opts.add_argument("--force-device-scale-factor=1")
        opts.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=opts)
        print("Using Chrome")
        return driver
    except Exception as e:
        print("Chrome failed (%s), trying Edge..." % e)
        opts = EdgeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--hide-scrollbars")
        opts.add_argument("--force-device-scale-factor=1")
        opts.add_argument("--disable-gpu")
        driver = webdriver.Edge(options=opts)
        print("Using Edge")
        return driver


def full_page_height(driver):
    return driver.execute_script(
        "return Math.max(document.body.scrollHeight, "
        "document.documentElement.scrollHeight);"
    )


def _scroll_through(driver):
    """Scroll top-to-bottom to trigger lazy images and reveal animations."""
    h = full_page_height(driver)
    y = 0
    while y < h:
        driver.execute_script("window.scrollTo(0, arguments[0]);", y)
        time.sleep(0.15)
        y += 600
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)


def shoot(driver, width, name, full=False, view_height=900):
    # Keep the layout viewport at a normal height so 100svh stays correct.
    driver.set_window_size(width, view_height)
    driver.get(URL)
    time.sleep(1.8)  # let fonts, images, and reveal animations settle

    path = OUT / name

    if full:
        _scroll_through(driver)
        # Full-page capture WITHOUT resizing the window: CDP captureBeyondViewport.
        metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
        css = metrics.get("cssContentSize") or metrics.get("contentSize")
        full_w = int(css["width"])
        full_h = int(css["height"])
        result = driver.execute_cdp_cmd("Page.captureScreenshot", {
            "format": "png",
            "captureBeyondViewport": True,
            "fromSurface": True,
            "clip": {"x": 0, "y": 0, "width": full_w, "height": full_h, "scale": 1},
        })
        path.write_bytes(base64.b64decode(result["data"]))
    else:
        driver.save_screenshot(str(path))

    print("saved", path)


def main():
    driver = make_driver()
    try:
        # Desktop above-the-fold
        shoot(driver, 1440, "desktop-hero.png", full=False, view_height=900)
        # Desktop full page
        shoot(driver, 1440, "desktop-full.png", full=True)
        # Mobile above-the-fold
        shoot(driver, 390, "mobile-hero.png", full=False, view_height=844)
        # Mobile full page
        shoot(driver, 390, "mobile-full.png", full=True)
    finally:
        driver.quit()
    print("\nDone. Screenshots in:", OUT)


if __name__ == "__main__":
    main()
