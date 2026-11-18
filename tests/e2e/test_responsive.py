import pytest
from playwright.sync_api import expect


@pytest.mark.e2e
@pytest.mark.responsive
def test_desktop_viewport_home_layout(home_page, test_data):
    vp = test_data["viewports"]["desktop"]
    home_page.page.set_viewport_size(vp)
    home_page.open_home()
    expect(home_page.navigation).to_be_visible()
    expect(home_page.footer).to_be_visible()
    home_page.verify_no_horizontal_overflow()


@pytest.mark.e2e
@pytest.mark.responsive
def test_mobile_viewport_home_layout(home_page, test_data):
    vp = test_data["viewports"]["mobile"]
    home_page.page.set_viewport_size(vp)
    home_page.open_home()
    expect(home_page.page.locator("body")).to_be_visible()
    expect(home_page.main_heading).to_be_visible()
    home_page.verify_no_horizontal_overflow()


@pytest.mark.e2e
@pytest.mark.responsive
def test_mobile_viewport_products_catalog(home_page, test_data):
    vp = test_data["viewports"]["mobile"]
    home_page.page.set_viewport_size(vp)
    home_page.open_products()
    expect(home_page.product_links.first).to_be_visible()
    home_page.verify_no_horizontal_overflow()


@pytest.mark.e2e
@pytest.mark.responsive
def test_tablet_viewport_products_catalog(home_page, test_data):
    vp = test_data["viewports"]["tablet"]
    home_page.page.set_viewport_size(vp)
    home_page.open_products()
    expect(home_page.product_links.first).to_be_visible()
    home_page.verify_no_horizontal_overflow()
