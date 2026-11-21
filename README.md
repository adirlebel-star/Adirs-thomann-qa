# Thomann QA (pytest + Playwright)

30 automated tests for https://www.thomannmusic.com/ - homepage, search, product page, basket, navigation and SEO/responsive checks.

## Setup

    python -m venv .venv
    .venv\Scripts\activate          # Windows PowerShell
    pip install -r requirements.txt
    playwright install chromium

## Run

    pytest -rs                      # all 30 tests, report in report.html
    pytest --headed                 # watch the browser
    pytest -m smoke                 # one group: smoke, search, product, cart, nav, seo
    pytest -k test_20               # a single test

## Note: site rate limiting

The site sits behind bot protection and returns HTTP 429 / "Just a moment" if it
gets too many requests. When that happens the affected tests are **skipped**
(not failed) - run `pytest -rs` to see the reason.

If many tests are skipped, wait a few minutes and run the groups one at a time:

    foreach ($m in "smoke","search","nav","product","cart","seo") { pytest -m $m -rs; Start-Sleep -Seconds 120 }

Each group overwrites `report.html`, so read the results from the terminal summary.

## Fixing selectors

If a test fails because of a selector, run `playwright codegen https://www.thomannmusic.com/`
and update the locators in `utils.py` (SEARCH_BOX, PRODUCT_LINK, COOKIE_BUTTON) or in the test.
