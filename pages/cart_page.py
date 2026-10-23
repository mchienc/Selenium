"""
CartPage: Quản lý trang chi tiết giỏ hàng (https://www.saucedemo.com/cart.html).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://www.saucedemo.com/cart.html"

    # Locators
    TITLE = (By.CLASS_NAME, "title")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_cart_item_names(self) -> list[str]:
        """Lấy danh sách tên các sản phẩm có trong giỏ hàng."""
        if not self.is_visible(self.CART_ITEM_NAMES):
            return []
        elements = self.find_all(self.CART_ITEM_NAMES)
        return [elem.text.strip() for elem in elements]

    def click_checkout(self):
        """Nhấn nút Tiến hành thanh toán (Checkout)."""
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one.html")

    def remove_item_by_name(self, product_name: str):
        """Xóa một sản phẩm khỏi giỏ hàng theo tên sản phẩm."""
        slug = product_name.lower().replace(" ", "-")
        remove_btn = (By.ID, f"remove-{slug}")
        self.click(remove_btn)
