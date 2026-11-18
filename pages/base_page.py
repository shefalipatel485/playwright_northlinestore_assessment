from urllib.parse import urljoin
from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page, base_url: str = "https://ecomcicid.netlify.app"):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/"):
        target_url = path if path.startswith("http") else urljoin(f"{self.base_url}/", path.lstrip("/"))
        self.page.goto(target_url, wait_until="domcontentloaded")
        return self

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    @property
    def navigation(self) -> Locator:
        return self.page.get_by_role("navigation").first

    @property
    def footer(self) -> Locator:
        return self.page.get_by_role("contentinfo").first

    @property
    def cart_link(self) -> Locator:
        return self.page.locator("a[href*='/cart'], button:has-text('Cart')").first

    def go_to_cart(self):
        if self.cart_link.count() > 0 and self.cart_link.is_visible():
            self.cart_link.click()
        else:
            self.open("/cart")

    def verify_no_horizontal_overflow(self):
        has_overflow = self.page.evaluate(
            "document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
        assert not has_overflow, "Horizontal scrollbar overflow detected on viewport"
