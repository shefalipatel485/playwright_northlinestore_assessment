import re
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.e2e
def test_product_listing_visible(home_page):
    home_page.open_products()
    expect(home_page.product_links.first).to_be_visible()


@pytest.mark.e2e
def test_product_card_has_image_and_name(home_page):
    home_page.open_products()
    first_product = home_page.product_links.first
    expect(first_product).to_be_visible()
    expect(first_product.locator("img").first).to_be_visible()
    expect(first_product).not_to_be_empty()


@pytest.mark.smoke
@pytest.mark.e2e
def test_open_product_details_page(home_page, product_page):
    home_page.open_products()
    home_page.open_first_product()
    expect(home_page.page).to_have_url(re.compile(r"/products/.+"))
    expect(product_page.product_title).to_be_visible()
    expect(product_page.product_image).to_be_visible()
    expect(product_page.add_to_cart_button).to_be_visible()


@pytest.mark.e2e
def test_search_input_available(home_page):
    home_page.open_products()
    expect(home_page.search_input).to_be_visible()


@pytest.mark.e2e
@pytest.mark.regression
def test_search_valid_product_filters_results(home_page):
    home_page.open_products()
    names = home_page.get_visible_product_names()
    assert len(names) > 0, "Expected at least one product on catalog page"
    keyword = names[0].split()[0]
    home_page.search_product(keyword)
    expect(home_page.product_links.first).to_be_visible()
    expect(home_page.page.locator("main")).to_contain_text(keyword, ignore_case=True)


@pytest.mark.e2e
@pytest.mark.regression
def test_search_no_results_state(home_page, test_data):
    home_page.open_products()
    invalid_query = test_data["search_queries"]["invalid"][0]
    home_page.search_product(invalid_query)
    no_results_locator = home_page.page.get_by_text(
        re.compile(r"no\s*(products|results|items)|not\s*found|0\s*products", re.IGNORECASE)
    ).first
    if no_results_locator.count() > 0:
        expect(no_results_locator).to_be_visible()
    else:
        expect(home_page.product_links).to_have_count(0)


@pytest.mark.e2e
@pytest.mark.regression
def test_clear_search_restores_catalog(home_page, test_data):
    home_page.open_products()
    initial_count = home_page.product_links.count()
    assert initial_count > 0
    home_page.search_product(test_data["search_queries"]["invalid"][0])
    home_page.clear_search()
    expect(home_page.product_links.first).to_be_visible()
