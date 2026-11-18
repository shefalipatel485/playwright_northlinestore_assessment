import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.e2e
def test_home_page_loads(home_page, test_data):
    expect(home_page.page).to_have_title(test_data["app"]["expected_title"])


@pytest.mark.smoke
@pytest.mark.e2e
def test_home_page_body_and_heading_visible(home_page):
    expect(home_page.page.locator("body")).to_be_visible()
    expect(home_page.main_heading).to_be_visible()


@pytest.mark.smoke
@pytest.mark.e2e
def test_navigation_visible_and_links_work(home_page):
    expect(home_page.navigation).to_be_visible()
    home_page.navigate_to_products()
    expect(home_page.page).to_have_url(f"{home_page.base_url}/products")


@pytest.mark.e2e
def test_footer_visible(home_page):
    expect(home_page.footer).to_be_visible()


@pytest.mark.e2e
@pytest.mark.regression
def test_https_protocol_enforced(home_page):
    assert home_page.get_current_url().startswith("https://")
