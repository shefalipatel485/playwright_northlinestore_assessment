import json
from pathlib import Path
import pytest
from faker import Faker

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

DATA_PATH = Path(__file__).parent / "data" / "test_data.json"


@pytest.fixture(scope="session")
def test_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def base_url(test_data):
    return test_data["app"]["base_url"]


@pytest.fixture(scope="session")
def api_base_url(test_data):
    return test_data["api"]["base_url"]


@pytest.fixture
def faker_instance():
    fake = Faker()
    Faker.seed(42)
    return fake


@pytest.fixture
def synthetic_customer(faker_instance):
    return {
        "full_name": faker_instance.name(),
        "email": faker_instance.safe_email(),
        "phone": faker_instance.msisdn()[:10],
        "address": faker_instance.street_address(),
        "city": faker_instance.city(),
        "postal_code": faker_instance.postcode(),
        "country": "United States",
    }


@pytest.fixture
def shop_page(page, base_url):
    page.goto(base_url, wait_until="domcontentloaded")
    return page


@pytest.fixture
def home_page(page, base_url):
    hp = HomePage(page, base_url)
    hp.open_home()
    return hp


@pytest.fixture
def product_page(page, base_url):
    return ProductPage(page, base_url)


@pytest.fixture
def cart_page(page, base_url):
    return CartPage(page, base_url)


@pytest.fixture
def checkout_page(page, base_url):
    return CheckoutPage(page, base_url)
