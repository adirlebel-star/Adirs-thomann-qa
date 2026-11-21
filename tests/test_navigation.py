import re
import pytest
from playwright.sync_api import Page, expect
from utils import open_page

pytestmark = pytest.mark.nav

GUITARS = "a[href$='guitars_and_basses.html']:visible"


def test_14_category_link_leads_to_category_page(home: Page):
    home.locator(GUITARS).first.click()
    expect(home).to_have_url(re.compile("guitars_and_basses"))


def test_15_browser_back_returns_home(home: Page):
    home.locator(GUITARS).first.click()
    home.wait_for_url(re.compile("guitars_and_basses"))
    home.go_back()
    expect(home).to_have_url(re.compile(r"thomannmusic\.com(/|/index\.html)?$"))


def test_16_contact_link_exists(home: Page):
    expect(home.locator("a[href$='compinfo_contact.html']").first).to_be_attached()


def test_17_language_is_declared(home: Page):
    declared = home.evaluate(
        "() => !!document.documentElement.lang || "
        "!!document.querySelector('meta[http-equiv=\"Content-Language\" i], meta[name=\"Content-Language\" i]')"
    )
    assert declared


def test_18_unknown_page_returns_404_or_not_found(page: Page):
    response = open_page(page, "/this-page-does-not-exist-12345.html")
    not_found_text = page.get_by_text(re.compile("not found|404|doesn.t exist", re.I)).count()
    assert (response is not None and response.status == 404) or not_found_text > 0
