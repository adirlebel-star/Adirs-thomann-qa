import re
import pytest
from playwright.sync_api import Page

COOKIE_BUTTON = re.compile(r"alright", re.I)
SEARCH_BOX = (
    "input[type='search'], input[name='sw'], input[placeholder*='earch' i], "
    "input[aria-label='Search'], [role='combobox'][aria-label='Search']"
)
# product links look like "xxx.htm?type=quickSearch" or "xxx.htm"
PRODUCT_LINK = "a[href*='.htm?'], a[href$='.htm']"
SAMPLE_PRODUCT = "/shure_sm58.htm"
ADD_TO_BASKET = re.compile(r"add to basket", re.I)

# The consent bar overlays the page and intercepts clicks.
_HIDE_CONSENT_CSS = ".spicy-consent-wrapper{display:none !important}"


def skip_if_blocked(page: Page, response=None) -> None:
    """The site sits behind bot protection. If we got blocked, skip instead of fail."""
    status = response.status if response is not None else None
    title = ""
    try:
        title = page.title()
    except Exception:
        pass
    if status in (403, 429) or title.lower().startswith("just a moment"):
        pytest.skip("Blocked by the site's bot protection / rate limit - wait and rerun later")


def dismiss_cookies(page: Page) -> None:
    """Close the cookie banner and make sure it can't block clicks."""
    try:
        btn = page.get_by_role("button", name=COOKIE_BUTTON).first
        btn.wait_for(state="visible", timeout=4000)
        btn.click(timeout=3000)
    except Exception:
        pass
    try:
        page.add_style_tag(content=_HIDE_CONSENT_CSS)
    except Exception:
        pass


def open_page(page: Page, path: str = "/"):
    """Open a path relative to base_url, handle blocking + cookies, return response."""
    response = page.goto(path, wait_until="domcontentloaded")
    skip_if_blocked(page, response)
    dismiss_cookies(page)
    return response


def search_for(page: Page, query: str) -> None:
    box = page.locator(SEARCH_BOX).first
    box.fill(query)
    box.press("Enter")
    page.wait_for_load_state("domcontentloaded")
    skip_if_blocked(page)
    dismiss_cookies(page)


def open_first_product(page: Page) -> None:
    page.locator(PRODUCT_LINK).first.click()
    page.wait_for_load_state("domcontentloaded")
    skip_if_blocked(page)
    dismiss_cookies(page)
