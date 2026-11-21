import pytest
from playwright.sync_api import Page
from utils import open_page, skip_if_blocked

pytestmark = pytest.mark.seo


def test_28_mobile_viewport_has_no_horizontal_scroll(page: Page):
    page.set_viewport_size({"width": 375, "height": 800})
    open_page(page, "/")
    overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 1


def test_29_meta_description_exists(home: Page):
    content = home.locator("meta[name='description']").get_attribute("content")
    assert content and len(content.strip()) > 20


def test_30_robots_txt_reachable(page: Page):
    response = page.request.get("/robots.txt")
    skip_if_blocked(page, response)
    assert response.ok
