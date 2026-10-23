"""
InventoryPage: Quản lý danh sách sản phẩm, lọc/sắp xếp, giỏ hàng và menu hệ thống.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "https://www.saucedemo.com/inventory.html"

    # Locators
    TITLE = (By.CLASS_NAME, "title")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_header_title(self) -> str:
        """Lấy tiêu đề trang (vd: 'Products')."""
        return self.get_text(self.TITLE)

    def sort_products_by(self, option_value: str):
        """
        Sắp xếp danh sách sản phẩm theo tùy chọn:
        - 'az'  : Name (A to Z)
        - 'za'  : Name (Z to A)
        - 'lohi': Price (low to high)
        - 'hilo': Price (high to low)
        """
        self.select_dropdown_by_value(self.SORT_DROPDOWN, option_value)

    def get_product_names(self) -> list[str]:
        """Lấy danh sách tên sản phẩm hiển thị trên màn hình."""
        elements = self.find_all(self.ITEM_NAMES)
        return [elem.text.strip() for elem in elements]

    def get_product_prices(self) -> list[float]:
        """Lấy danh sách giá sản phẩm dưới dạng số thực float."""
        elements = self.find_all(self.ITEM_PRICES)
        return [float(elem.text.replace("$", "").strip()) for elem in elements]

    def add_product_to_cart_by_id(self, button_id: str):
        """Thêm sản phẩm vào giỏ hàng bằng id nút Add to Cart."""
        self.click((By.ID, button_id))

    def add_first_product_to_cart(self):
        """Thêm sản phẩm đầu tiên hiển thị vào giỏ hàng."""
        first_btn = (By.CSS_SELECTOR, ".inventory_item button.btn_inventory")
        self.click(first_btn)

    def get_cart_badge_count(self) -> int:
        """Lấy số lượng sản phẩm hiển thị trên huy hiệu giỏ hàng."""
        if self.is_visible(self.CART_BADGE):
            text = self.get_text(self.CART_BADGE)
            return int(text) if text.isdigit() else 0
        return 0

    def go_to_cart(self):
        """Nhấn biểu tượng giỏ hàng để chuyển sang trang Giỏ hàng."""
        self.js_click(self.CART_LINK)
        self.wait_for_url_contains("cart.html")

    def logout(self):
        """Mở menu điều hướng và thực hiện đăng xuất."""
        self.js_click(self.BURGER_MENU_BUTTON)
        self.js_click(self.LOGOUT_LINK)
        self.wait_for_url_to_be("https://www.saucedemo.com/")
