from playwright.sync_api import Locator, expect
from pages.base_page import BasePage


class ProductPage(BasePage):
    @property
    def product_title(self) -> Locator:
        return self.page.get_by_role("heading", level=1).or_(
            self.page.get_by_role("heading")
        ).first

    @property
    def product_image(self) -> Locator:
        return self.page.locator("main img").first

    @property
    def product_price(self) -> Locator:
        return self.page.locator("main").get_by_text("$", exact=False).first

    @property
    def add_to_cart_button(self) -> Locator:
        return self.page.get_by_role("button", name="Add to Cart", exact=False).or_(
            self.page.get_by_role("button", name="Add to Bag", exact=False)
        ).first

    def add_to_cart(self):
        btn = self.add_to_cart_button
        expect(btn).to_be_visible()
        expect(btn).to_be_enabled()
        btn.click()

    def get_product_name_text(self) -> str:
        expect(self.product_title).to_be_visible()
        return self.product_title.inner_text().strip()
