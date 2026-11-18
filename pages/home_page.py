from playwright.sync_api import Locator, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    def open_home(self):
        return self.open("/")

    def open_products(self):
        return self.open("/products")

    @property
    def main_heading(self) -> Locator:
        return self.page.get_by_role("heading").first

    @property
    def products_nav_link(self) -> Locator:
        return self.page.get_by_role("link", name="Products", exact=False).first

    @property
    def product_links(self) -> Locator:
        return self.page.locator("main a[href*='/products/']")

    @property
    def search_input(self) -> Locator:
        return self.page.get_by_role("searchbox").or_(
            self.page.locator("input[type='search'], input[placeholder*='Search' i]")
        ).first

    @property
    def category_filter(self) -> Locator:
        return self.page.locator("select, [role='combobox'], button:has-text('Category'), button:has-text('All')").first

    @property
    def sort_select(self) -> Locator:
        return self.page.locator("select[aria-label*='sort' i], select[name*='sort' i], select").last

    def navigate_to_products(self):
        if self.products_nav_link.count() > 0 and self.products_nav_link.is_visible():
            self.products_nav_link.click()
        else:
            self.open_products()

    def search_product(self, query: str):
        search = self.search_input
        expect(search).to_be_visible()
        search.fill(query)
        search.press("Enter")

    def clear_search(self):
        search = self.search_input
        expect(search).to_be_visible()
        search.fill("")
        search.press("Enter")

    def open_first_product(self):
        first_card = self.product_links.first
        expect(first_card).to_be_visible()
        first_card.click()

    def get_visible_product_names(self) -> list[str]:
        count = self.product_links.count()
        names = []
        for i in range(count):
            text = self.product_links.nth(i).inner_text().strip()
            if text:
                names.append(text.splitlines()[0].strip())
        return names
