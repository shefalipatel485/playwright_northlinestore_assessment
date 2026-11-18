import re
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.e2e
def test_add_product_to_cart(home_page, product_page, cart_page):
    home_page.open_products()
    home_page.open_first_product()
    selected_name = product_page.get_product_name_text()
    product_page.add_to_cart()
    cart_page.open_cart()
    expect(cart_page.page.locator("main")).to_contain_text(selected_name, ignore_case=True)


@pytest.mark.e2e
@pytest.mark.regression
def test_update_cart_item_quantity(home_page, product_page, cart_page):
    home_page.open_products()
    home_page.open_first_product()
    product_page.add_to_cart()
    cart_page.open_cart()
    if cart_page.increase_qty_button.count() > 0:
        cart_page.increase_quantity()
        expect(cart_page.page.locator("main")).to_contain_text("2")


@pytest.mark.e2e
@pytest.mark.regression
def test_remove_item_from_cart(home_page, product_page, cart_page):
    home_page.open_products()
    home_page.open_first_product()
    product_page.add_to_cart()
    cart_page.open_cart()
    if cart_page.remove_button.count() > 0:
        cart_page.remove_first_item()
        expect(cart_page.empty_cart_message).to_be_visible()


@pytest.mark.e2e
@pytest.mark.regression
def test_cart_persists_after_page_reload(home_page, product_page, cart_page):
    home_page.open_products()
    home_page.open_first_product()
    selected_name = product_page.get_product_name_text()
    product_page.add_to_cart()
    cart_page.open_cart()
    cart_page.page.reload(wait_until="domcontentloaded")
    expect(cart_page.page.locator("main")).to_contain_text(selected_name, ignore_case=True)


@pytest.mark.e2e
@pytest.mark.regression
def test_checkout_validation_blocks_empty_submission(home_page, product_page, cart_page, checkout_page):
    home_page.open_products()
    home_page.open_first_product()
    product_page.add_to_cart()
    cart_page.open_cart()
    if cart_page.checkout_button.count() > 0:
        cart_page.proceed_to_checkout()
    else:
        checkout_page.open_checkout()
    if checkout_page.submit_order_button.count() > 0:
        checkout_page.submit_order()
        assert "/checkout" in checkout_page.get_current_url() or checkout_page.page.locator(":invalid").count() > 0


@pytest.mark.e2e
@pytest.mark.regression
def test_checkout_with_synthetic_customer_data(
    home_page, product_page, cart_page, checkout_page, synthetic_customer
):
    home_page.open_products()
    home_page.open_first_product()
    product_page.add_to_cart()
    cart_page.open_cart()
    if cart_page.checkout_button.count() > 0:
        cart_page.proceed_to_checkout()
    else:
        checkout_page.open_checkout()
    checkout_page.fill_customer_details(synthetic_customer)
    if checkout_page.submit_order_button.count() > 0:
        checkout_page.submit_order()
        confirmation = checkout_page.page.get_by_text(
            re.compile(r"thank you|order confirmed|order placed|success", re.IGNORECASE)
        ).first
        expect(confirmation).to_be_visible()
