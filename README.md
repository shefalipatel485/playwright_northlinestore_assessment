# Northline Store — Playwright & Pytest Automation Framework

End-to-end UI, API contract, network mocking, and cross-browser responsive test automation suite for **Northline Store** (`https://ecomcicid.netlify.app`).

---

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml              # GitHub Actions CI/CD (API + Chromium/Firefox/WebKit matrix)
├── data/
│   └── test_data.json             # Centralized URLs, SLAs, viewports & search test data
├── docs/
│   ├── API_DOCUMENTATION.md       # Discovered MockAPI endpoints, schemas & scenarios
│   ├── SECURITY_CHECKLIST.md      # Security & synthetic test data verification checklist
│   ├── TEST_PLAN.md               # Test strategy, scope, browsers & acceptance criteria
│   └── TEST_SUMMARY.md            # Coverage matrix & CI/CD execution checklist
├── pages/
│   ├── __init__.py
│   ├── base_page.py               # Shared navigation, URL helpers & viewport overflow checks
│   ├── home_page.py               # Homepage & Product Catalog Page Object
│   ├── product_page.py            # Product Detail Page Object
│   ├── cart_page.py               # Shopping Cart Page Object
│   └── checkout_page.py           # Checkout Form Page Object
├── tests/
│   ├── api/
│   │   ├── test_api.py            # REST CRUD, jsonschema validation, SLA & UI-API consistency
│   │   └── test_network.py        # Playwright page.route() network mocking & error simulation
│   └── e2e/
│       ├── test_home.py           # Homepage, navigation, footer & HTTPS smoke tests
│       ├── test_products.py       # Catalog listing, product details, search & reset tests
│       ├── test_cart.py           # Add to cart, quantity, removal, reload persistence & checkout
│       └── test_responsive.py     # Desktop (1366x768), Tablet (768x1024) & Mobile (390x844)
├── .gitignore                     # Excludes __pycache__, .pyc, reports/ & test-results/
├── conftest.py                    # Pytest fixtures (POM objects, test_data, Faker synthetic data)
├── pytest.ini                     # Markers, HTML report, trace & screenshot configuration
├── README.md                      # Setup, architecture & execution guide
└── requirements.txt               # Project dependencies
```

---

## Setup & Installation

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate           # Windows
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browser binaries:**
   ```bash
   playwright install --with-deps
   ```

---

## Running Tests

| Command | Description |
| :--- | :--- |
| `pytest` | Run the full suite with HTML reporting, failure traces, and screenshots |
| `pytest -m smoke` | Run critical smoke tests |
| `pytest tests/e2e` | Run all E2E & responsive browser tests |
| `pytest tests/api` | Run API schema, CRUD, and network interception tests |
| `pytest -m responsive` | Run desktop, tablet, and mobile viewport tests |
| `pytest --browser firefox` | Execute browser tests on Firefox (`chromium`, `firefox`, `webkit`) |
| `pytest -n auto` | Execute tests in parallel via `pytest-xdist` |

---

## Test Coverage Summary

- **E2E UI Suite (22 tests):** Homepage, navigation, catalog cards, product details, search & clear, cart add/update/remove/persistence, checkout validation & synthetic Faker order flow.
- **Responsive Suite (4 tests):** Desktop (`1366x768`), Tablet (`768x1024`), and Mobile (`390x844`) layout & horizontal overflow verification.
- **API & Network Suite (13 tests):** `jsonschema` validation, CRUD lifecycle with cleanup, response time SLA, UI-API catalog consistency, and `page.route()` network mocking (`200`, empty `[]`, and `500` error states).
- **CI/CD Pipeline:** Automated GitHub Actions workflow running on push, pull requests, nightly schedule, and manual dispatch across Chromium, Firefox, and WebKit with artifact uploads for HTML reports, failure screenshots, and Playwright traces.
