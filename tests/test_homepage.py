import re
import pytest
from playwright.sync_api import Page, expect
from utils import open_page, SEARCH_BOX

pytestmark = pytest.mark.smoke


def test_01_homepage_returns_200(page: Page):
    response = open_page(page, "/")
    assert response is not None and response.status == 200


def test_02_homepage_title_is_correct(home: Page):
    expect(home).to_have_title(re.compile("musical instruments", re.I))


def test_03_homepage_uses_https(home: Page):
    assert home.url.startswith("https://")


def test_04_search_box_visible(home: Page):
    expect(home.locator(SEARCH_BOX).first).to_be_visible()


def test_05_main_navigation_visible(home: Page):
    expect(home.locator("nav, header").first).to_be_visible()


def test_06_footer_visible(home: Page):
    footer = home.locator("footer").first
    footer.scroll_into_view_if_needed()
    expect(footer).to_be_visible()
