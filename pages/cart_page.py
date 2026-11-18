import re
from playwright.sync_api import Locator, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def open_cart(self):
        return self.open("/cart")

    @property
    def cart_items(self) -> Locator:
        return self.page.locator(
            '[data-testid="cart-item"], main article, main li:has(button), main tr:has(button)'
        )

    @property
    def empty_cart_message(self) -> Locator:
        return self.page.get_by_text(re.compile(r"empty|no items", re.IGNORECASE)).first

    @property
    def increase_qty_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"^\+$|increase|plus|add", re.IGNORECASE)).first

    @property
    def decrease_qty_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"^-$|decrease|minus", re.IGNORECASE)).first

    @property
    def remove_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"remove|delete", re.IGNORECASE)).first

    @property
    def checkout_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r"checkout|proceed", re.IGNORECASE)).or_(
            self.page.get_by_role("link", name=re.compile(r"checkout|proceed", re.IGNORECASE))
        ).first

    def increase_quantity(self):
        expect(self.increase_qty_button).to_be_visible()
        self.increase_qty_button.click()

    def decrease_quantity(self):
        expect(self.decrease_qty_button).to_be_visible()
        self.decrease_qty_button.click()

    def remove_first_item(self):
        expect(self.remove_button).to_be_visible()
        self.remove_button.click()

    def proceed_to_checkout(self):
        expect(self.checkout_button).to_be_visible()
        self.checkout_button.click()
