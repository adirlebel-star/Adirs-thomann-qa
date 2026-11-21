import re
import pytest
from playwright.sync_api import Page, expect
from utils import ADD_TO_BASKET

pytestmark = pytest.mark.product


def test_19_product_page_has_heading(product_page: Page):
    expect(product_page.get_by_role("heading", level=1)).to_contain_text("Shure SM58")


def test_20_product_page_shows_price(product_page: Page):
    expect(product_page.get_by_text(re.compile(r"\$\s?\d")).first).to_be_visible()


def test_21_product_page_has_image(product_page: Page):
    expect(product_page.locator("img[alt*='SM58']:visible").first).to_be_visible()


def test_22_add_to_basket_button_visible(product_page: Page):
    expect(product_page.get_by_text(ADD_TO_BASKET).first).to_be_visible()


def test_23_product_page_title_contains_product_name(product_page: Page):
    expect(product_page).to_have_title(re.compile("SM58", re.I))


def test_24_product_page_shows_stock_info(product_page: Page):
    expect(product_page.get_by_text(
        re.compile("in stock|available at short notice|delivery", re.I)
    ).first).to_be_visible()
