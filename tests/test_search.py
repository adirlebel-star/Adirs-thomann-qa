import re
import pytest
from playwright.sync_api import Page, expect
from utils import open_page, search_for, SEARCH_BOX, PRODUCT_LINK

pytestmark = pytest.mark.search


def test_07_search_via_box_changes_url(home: Page):
    search_for(home, "ukulele")
    expect(home).to_have_url(re.compile(r"search_dir|sw=", re.I))


def test_08_results_page_heading_shows_query(home: Page):
    search_for(home, "ukulele")
    expect(home.get_by_role("heading", level=1)).to_contain_text(re.compile("ukulele", re.I))


def test_09_direct_search_url_has_products(page: Page):
    open_page(page, "/search_dir.html?sw=ukulele")
    expect(page.locator(PRODUCT_LINK).first).to_be_attached()


def test_10_gibberish_query_shows_no_results(page: Page):
    open_page(page, "/search_dir.html?sw=zzxqwvkj123456")
    expect(page.get_by_text(re.compile(
        r"no results|nothing found|0 results|no products|did not find|didn.t find", re.I
    )).first).to_be_visible()


def test_11_query_kept_in_search_box(home: Page):
    search_for(home, "ukulele")
    expect(home.locator(SEARCH_BOX).first).to_have_value(re.compile("ukulele", re.I))


def test_12_special_characters_do_not_break_search(page: Page):
    response = open_page(page, "/search_dir.html?sw=boss%20%26%20roland")
    assert response is not None and response.status < 400


def test_13_empty_search_does_not_crash(home: Page):
    box = home.locator(SEARCH_BOX).first
    box.fill("")
    box.press("Enter")
    home.wait_for_load_state("domcontentloaded")
    expect(home.locator("body")).to_be_visible()
