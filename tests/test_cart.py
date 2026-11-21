import re
import time
import pytest
from playwright.sync_api import Page, expect
from utils import ADD_TO_BASKET, open_page, dismiss_cookies, skip_if_blocked

pytestmark = pytest.mark.cart

BASKET_LINK = "a[href$='basket.html']"
# Texts that typically show up after an item was added (NOT present before the click)
ADDED_TEXT = re.compile(
    r"added to|has been added|continue shopping|go to (the )?basket|view (the )?basket",
    re.I,
)


def _basket_signature(page: Page) -> str:
    """Text + aria-label of the header basket link (usually contains the item counter)."""
    link = page.locator(BASKET_LINK).first
    try:
        return (link.inner_text() or "").strip() + "|" + (link.get_attribute("aria-label") or "")
    except Exception:
        return ""


def test_25_empty_basket_page_loads(page: Page):
    response = open_page(page, "/basket.html")
    assert response is not None and response.status < 400


def test_26_add_product_to_basket(product_page: Page):
    """Click 'Add to Basket' and verify it from the product page itself.

    We do NOT open basket.html afterwards (it triggers the site's rate limit).
    Success = any of: redirect to a basket page, a basket dialog, an 'added' message,
    or a change in the header basket counter.
    """
    page = product_page
    dismiss_cookies(page)

    sig_before = _basket_signature(page)
    hits_before = page.get_by_text(ADDED_TEXT).count()

    page.get_by_text(ADD_TO_BASKET).first.click()

    added = False
    deadline = time.time() + 10
    while time.time() < deadline and not added:
        skip_if_blocked(page)
        if "basket" in page.url.lower():
            added = True
        elif page.get_by_role("dialog").filter(
            has_text=re.compile("basket", re.I)
        ).first.is_visible():
            added = True
        elif page.get_by_text(ADDED_TEXT).count() > hits_before:
            added = True
        elif _basket_signature(page) != sig_before:
            added = True
        else:
            page.wait_for_timeout(500)

    assert added, "No sign that the item was added (no redirect, dialog, message or counter change)"


def test_27_basket_link_exists(home: Page):
    expect(home.locator(BASKET_LINK).first).to_be_attached()