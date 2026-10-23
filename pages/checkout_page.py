"""
CheckoutPage: Quản lý các bước trong quy trình thanh toán đặt hàng (Checkout).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Step One Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Step Two Locators
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")

    # Complete Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def enter_shipping_info(self, first_name: str, last_name: str, postal_code: str):
        """Nhập thông tin giao hàng của khách hàng."""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def click_continue(self):
        """Nhấn nút Tiếp tục (Continue) sang bước tổng kết đơn."""
        self.js_click(self.CONTINUE_BUTTON)
        self.wait_for_url_contains("checkout-step-two.html")

    def click_finish(self):
        """Nhấn nút Hoàn tất (Finish) để xác nhận đặt hàng."""
        self.js_click(self.FINISH_BUTTON)
        self.wait_for_url_contains("checkout-complete.html")

    def get_complete_header_text(self) -> str:
        """Lấy thông điệp xác nhận hoàn tất đặt hàng."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi nếu bỏ trống thông tin giao hàng."""
        return self.get_text(self.ERROR_CONTAINER)
