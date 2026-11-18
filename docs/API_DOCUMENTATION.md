# Northline Store – API Documentation

## 1. Project Information

- **Application:** Northline Store (`https://ecomcicid.netlify.app/`)
- **Discovered Backend API:** `https://681444af225ff1af16285b31.mockapi.io/electronicapi`
- **Automation Stack:** Python, Pytest, `requests`, `jsonschema`, and Playwright (`page.route`)

## 2. Endpoint Inventory

| ID | Feature | Method | Endpoint | Status |
|---|---|---|---|---|
| API-01 | Get all products | `GET` | `/electronicapi` | Verified |
| API-02 | Get single product | `GET` | `/electronicapi/{id}` | Verified |
| API-03 | Invalid product ID | `GET` | `/electronicapi/99999999` | Verified (`404`) |
| API-04 | Create product | `POST` | `/electronicapi` | Verified (`201`) |
| API-05 | Update product | `PATCH` | `/electronicapi/{id}` | Verified (`200`) |
| API-06 | Delete product | `DELETE` | `/electronicapi/{id}` | Verified (`200`) |

## 3. Product JSON Schema

Validated automatically in `tests/api/test_api.py` via `jsonschema`:

```json
{
  "id": "1",
  "name": "Skullcandy Crusher Evo",
  "price": "199",
  "brand": "Skullcandy",
  "category": "Headphones",
  "rating": "4.7",
  "stock": "15"
}
```

## 4. Network Interception & Mocking (`tests/api/test_network.py`)

Playwright `page.route("**/electronicapi**", ...)` is used to verify:
- Deterministic rendering of mocked product payloads (`HTTP 200`).
- Empty catalog handling (`HTTP 200` with `[]`).
- Graceful UI resilience during backend `HTTP 500` errors.
- Outgoing browser XHR/Fetch request verification.
