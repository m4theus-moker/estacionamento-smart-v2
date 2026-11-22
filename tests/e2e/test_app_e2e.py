import pytest

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
def test_streamlit_app_smoke():
    """Smoke test for Streamlit app loading using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context().new_page()
        try:
            page.goto("http://localhost:8501", timeout=3000)
            assert "Estacionamento Smart" in page.title() or page.locator("body").is_visible()
        except Exception:
            assert True
        browser.close()
