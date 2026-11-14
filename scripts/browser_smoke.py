"""Chrome smoke tests and screenshots for the public Utility Shelf UI.

Run against a local Uvicorn server, not the deployed Space.
"""

import os
import re
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE = os.environ.get("SHELF_BASE_URL", "http://127.0.0.1:7860")
OUTPUT = Path(os.environ.get("SHELF_SCREENSHOTS", "/tmp/shelf-browser-shots"))
OUTPUT.mkdir(parents=True, exist_ok=True)


def rgb(css: str) -> tuple[float, float, float]:
    values = re.findall(r"[\d.]+", css)
    return tuple(float(x) / 255 for x in values[:3])


def contrast(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    def luminance(values):
        converted = [(v / 12.92) if v <= .04045 else ((v + .055) / 1.055) ** 2.4
                     for v in values]
        return .2126 * converted[0] + .7152 * converted[1] + .0722 * converted[2]
    bright, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (bright + .05) / (dark + .05)


def smoke():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        desktop = browser.new_context(viewport={"width": 1440, "height": 900},
                                      device_scale_factor=1)
        page = desktop.new_page()
        page.goto(BASE + "/", wait_until="networkidle")
        page.get_by_role("heading", name="Good tools. Better workflows.").wait_for()
        assert "34" in page.locator(".stat-value").first.inner_text()
        page.screenshot(path=str(OUTPUT / "desktop-light.png"), full_page=True)

        page.keyboard.press("Control+k")
        page.get_by_role("dialog", name="Search tools").wait_for()
        page.locator("#modal-input").fill("PDF to Word")
        page.locator(".modal-item").first.click()
        page.wait_for_url("**/tools/pdf-to-word")
        assert page.get_by_role("heading", name="PDF to Word").count() == 1

        page.goto(BASE + "/tools/upper-case", wait_until="networkidle")
        page.get_by_role("button", name="Toggle colour theme").click()
        assert page.locator("html").get_attribute("data-theme") == "dark"
        page.locator("#tool-text").fill("Developer Quality")
        fg, bg = page.locator("#tool-text").evaluate(
            "(node) => {const c=getComputedStyle(node); return [c.color,c.backgroundColor]}"
        )
        ratio = contrast(rgb(fg), rgb(bg))
        assert ratio >= 7.0, f"Dark textarea contrast too low: {ratio:.2f}"
        page.screenshot(path=str(OUTPUT / "desktop-dark-tool.png"), full_page=True)

        page.get_by_role("button", name="Run utility").click()
        page.get_by_text("Completed successfully").wait_for(timeout=12000)
        assert "DEVELOPER QUALITY" in page.locator(".result-data").inner_text()
        page.get_by_role("button", name="Copy result").is_visible()

        mobile = browser.new_context(viewport={"width": 390, "height": 844},
                                     device_scale_factor=1, is_mobile=True, has_touch=True)
        small = mobile.new_page()
        small.goto(BASE + "/", wait_until="networkidle")
        assert small.get_by_role("heading", name="Good tools. Better workflows.").is_visible()
        assert small.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 3")
        small.get_by_role("button", name="Open menu").click()
        assert small.locator("body").evaluate("(node) => node.classList.contains('menu-open')")
        small.screenshot(path=str(OUTPUT / "mobile-menu.png"), full_page=True)
        small.get_by_role("button", name="Open menu").count()
        mobile.close()
        desktop.close()
        browser.close()
    print("Browser smoke tests passed; screenshots written to", OUTPUT)


if __name__ == "__main__":
    smoke()
