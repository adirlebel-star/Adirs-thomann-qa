import time
import pytest
from utils import open_page, search_for, SAMPLE_PRODUCT


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 800},
        "locale": "en-US",
    }


@pytest.fixture(autouse=True)
def polite_delay():
    """Pause between tests so we don't hammer the site (it rate-limits with HTTP 429)."""
    yield
    time.sleep(2.5)


@pytest.fixture
def home(page):
    open_page(page, "/")
    return page


@pytest.fixture
def results_page(page):
    open_page(page, "/")
    search_for(page, "ukulele")
    return page


@pytest.fixture
def product_page(page):
    open_page(page, SAMPLE_PRODUCT)
    return page
