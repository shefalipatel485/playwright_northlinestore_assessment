import time
import pytest
import requests
from jsonschema import validate

PRODUCT_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "brand", "category", "rating", "stock"],
    "properties": {
        "id": {"type": ["string", "integer"]},
        "name": {"type": "string", "minLength": 1},
        "price": {"type": ["string", "number"]},
        "brand": {"type": "string"},
        "category": {"type": "string"},
        "rating": {"type": ["string", "number"]},
        "stock": {"type": ["string", "integer"]},
    },
    "additionalProperties": True,
}

PRODUCT_LIST_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": PRODUCT_SCHEMA,
}


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_products(api_base_url):
    response = requests.get(api_base_url, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.api
def test_product_list_json_schema(api_base_url):
    response = requests.get(api_base_url, timeout=10)
    assert response.status_code == 200
    validate(instance=response.json(), schema=PRODUCT_LIST_SCHEMA)


@pytest.mark.api
def test_get_single_product_and_schema(api_base_url):
    list_response = requests.get(api_base_url, timeout=10)
    assert list_response.status_code == 200
    first_product = list_response.json()[0]
    product_id = first_product["id"]

    response = requests.get(f"{api_base_url}/{product_id}", timeout=10)
    assert response.status_code == 200
    product = response.json()
    validate(instance=product, schema=PRODUCT_SCHEMA)
    assert str(product["id"]) == str(product_id)
    assert product["name"] == first_product["name"]


@pytest.mark.api
def test_get_invalid_product_returns_404(api_base_url):
    response = requests.get(f"{api_base_url}/99999999", timeout=10)
    assert response.status_code in (400, 404)


@pytest.mark.api
def test_response_headers_and_content_type(api_base_url):
    response = requests.get(api_base_url, timeout=10)
    assert response.status_code == 200
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type


@pytest.mark.api
def test_api_response_time_sla(api_base_url, test_data):
    max_sla = test_data["api"]["max_response_time_sec"]
    start_time = time.perf_counter()
    response = requests.get(api_base_url, timeout=10)
    elapsed = time.perf_counter() - start_time
    assert response.status_code == 200
    assert elapsed < max_sla, f"API took {elapsed:.3f}s, exceeding {max_sla}s SLA"


@pytest.mark.api
def test_create_product_crud(api_base_url, faker_instance):
    new_product = {
        "name": f"Automation {faker_instance.word().capitalize()} Headphones",
        "price": str(faker_instance.random_int(min=50, max=500)),
        "brand": faker_instance.company(),
        "category": "Headphones",
        "rating": "4.6",
        "stock": "15",
        "description": "Created via Pytest API automation",
        "image": "https://picsum.photos/400/400",
    }
    response = requests.post(api_base_url, json=new_product, timeout=10)
    assert response.status_code == 201
    created = response.json()
    validate(instance=created, schema=PRODUCT_SCHEMA)
    assert created["name"] == new_product["name"]

    product_id = created["id"]
    try:
        del_resp = requests.delete(f"{api_base_url}/{product_id}", timeout=10)
        assert del_resp.status_code == 200
    finally:
        requests.delete(f"{api_base_url}/{product_id}", timeout=10)


@pytest.mark.api
def test_update_and_delete_product_crud(api_base_url, faker_instance):
    payload = {
        "name": f"Temp {faker_instance.word().capitalize()} Device",
        "price": "199",
        "brand": "NorthlineAudio",
        "category": "Electronics",
        "rating": "4.2",
        "stock": "8",
    }
    create_resp = requests.post(api_base_url, json=payload, timeout=10)
    assert create_resp.status_code == 201
    product_id = create_resp.json()["id"]

    try:
        patch_resp = requests.patch(
            f"{api_base_url}/{product_id}",
            json={"price": "249"},
            timeout=10,
        )
        assert patch_resp.status_code == 200
        assert str(patch_resp.json()["price"]) == "249"

        get_resp = requests.get(f"{api_base_url}/{product_id}", timeout=10)
        assert get_resp.status_code == 200
        assert str(get_resp.json()["price"]) == "249"

        del_resp = requests.delete(f"{api_base_url}/{product_id}", timeout=10)
        assert del_resp.status_code == 200

        verify_resp = requests.get(f"{api_base_url}/{product_id}", timeout=10)
        assert verify_resp.status_code in (400, 404)
    finally:
        requests.delete(f"{api_base_url}/{product_id}", timeout=10)


@pytest.mark.api
@pytest.mark.e2e
def test_api_and_ui_product_consistency(page, base_url, api_base_url):
    api_resp = requests.get(api_base_url, timeout=10)
    assert api_resp.status_code == 200
    api_products = api_resp.json()
    api_names = {p["name"].strip().lower() for p in api_products if p.get("name")}

    page.goto(f"{base_url}/products", wait_until="domcontentloaded")
    page.wait_for_selector("main a[href*='/products/']", timeout=10000)
    ui_text = page.locator("main").inner_text().lower()

    matched = [name for name in api_names if name in ui_text]
    assert len(matched) > 0, (
        f"Expected at least one API product name in UI catalog. API names: {list(api_names)[:5]}"
    )
