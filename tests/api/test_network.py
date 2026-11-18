import json
import pytest
from playwright.sync_api import expect


MOCK_PRODUCTS = [
    {
        "id": "101",
        "name": "Mocked Quantum ANC Headphones",
        "price": "299",
        "brand": "Northline",
        "category": "Headphones",
        "rating": "4.9",
        "stock": "12",
        "description": "Injected via Playwright page.route() network interception",
        "image": "https://picsum.photos/400/400",
    },
    {
        "id": "102",
        "name": "Mocked Studio Mechanical Keyboard",
        "price": "149",
        "brand": "Northline",
        "category": "Accessories",
        "rating": "4.8",
        "stock": "7",
        "description": "Mocked catalog item for deterministic UI verification",
        "image": "https://picsum.photos/400/400",
    },
]


@pytest.mark.api
@pytest.mark.e2e
def test_mock_api_products_rendered_in_ui(page, base_url):
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(MOCK_PRODUCTS),
        )

    page.route("**/electronicapi**", handle_route)
    page.goto(f"{base_url}/products", wait_until="domcontentloaded")

    expect(page.get_by_text("Mocked Quantum ANC Headphones")).to_be_visible()
    expect(page.get_by_text("Mocked Studio Mechanical Keyboard")).to_be_visible()


@pytest.mark.api
@pytest.mark.e2e
def test_mock_api_empty_catalog_response(page, base_url):
    page.route(
        "**/electronicapi**",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([]),
        ),
    )
    page.goto(f"{base_url}/products", wait_until="domcontentloaded")
    expect(page.locator("main a[href*='/products/']")).to_have_count(0)


@pytest.mark.api
@pytest.mark.e2e
def test_mock_api_500_server_error_graceful_handling(page, base_url):
    page.route(
        "**/electronicapi**",
        lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Internal Server Error"}),
        ),
    )
    page.goto(f"{base_url}/products", wait_until="domcontentloaded")
    # Verify app does not crash with blank screen
    expect(page.locator("body")).to_be_visible()
    expect(page.get_by_role("navigation").first).to_be_visible()


@pytest.mark.api
@pytest.mark.e2e
def test_intercept_and_verify_catalog_network_request(page, base_url):
    captured_requests = []

    def log_request(request):
        if "electronicapi" in request.url:
            captured_requests.append(request.url)

    page.on("request", log_request)
    page.goto(f"{base_url}/products", wait_until="networkidle")
    assert len(captured_requests) >= 1, "Expected browser to fetch product catalog from electronicapi"
