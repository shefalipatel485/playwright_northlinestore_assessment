import re
from playwright.sync_api import Locator, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def open_checkout(self):
        return self.open("/checkout")

    @property
    def name_input(self) -> Locator:
        return self.page.get_by_label(re.compile(r"name", re.IGNORECASE)).or_(
            self.page.locator("input[name*='name' i], input[placeholder*='name' i]")
        ).first

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_label(re.compile(r"email", re.IGNORECASE)).or_(
            self.page.locator("input[type='email'], input[name*='email' i]")
        ).first

    @property
    def address_input(self) -> Locator:
        return self.page.get_by_label(re.compile(r"address|street", re.IGNORECASE)).or_(
            self.page.locator("input[name*='address' i], textarea[name*='address' i], input[placeholder*='address' i]")
        ).first

    @property
    def city_input(self) -> Locator:
        return self.page.get_by_label(re.compile(r"city", re.IGNORECASE)).or_(
            self.page.locator("input[name*='city' i], input[placeholder*='city' i]")
        ).first

    @property
    def postal_input(self) -> Locator:
        return self.page.get_by_label(re.compile(r"zip|postal", re.IGNORECASE)).or_(
            self.page.locator("input[name*='zip' i], input[name*='postal' i], input[placeholder*='zip' i]")
        ).first

    @property
    def submit_order_button(self) -> Locator:
        return self.page.get_by_role(
            "button", name=re.compile(r"place order|submit|complete|pay", re.IGNORECASE)
        ).first

    def fill_customer_details(self, customer: dict):
        if self.name_input.count() > 0 and self.name_input.is_visible():
            self.name_input.fill(customer["full_name"])
        if self.email_input.count() > 0 and self.email_input.is_visible():
            self.email_input.fill(customer["email"])
        if self.address_input.count() > 0 and self.address_input.is_visible():
            self.address_input.fill(customer["address"])
        if self.city_input.count() > 0 and self.city_input.is_visible():
            self.city_input.fill(customer["city"])
        if self.postal_input.count() > 0 and self.postal_input.is_visible():
            self.postal_input.fill(customer["postal_code"])

    def submit_order(self):
        expect(self.submit_order_button).to_be_visible()
        self.submit_order_button.click()
