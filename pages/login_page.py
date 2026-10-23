"""
LoginPage: Quản lý các phần tử và hành vi trên trang đăng nhập (https://www.saucedemo.com/).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self):
        """Mở trang đăng nhập."""
        self.open_url(self.URL)
        return self

    def enter_username(self, username: str):
        """Nhập tên người dùng."""
        self.enter_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Nhập mật khẩu."""
        self.enter_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Nhấn nút Đăng nhập."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Tiện ích thực hiện chuỗi đăng nhập hoàn chỉnh."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Lấy nội dung thông báo lỗi khi đăng nhập không thành công."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Kiểm tra thông báo lỗi có hiển thị hay không."""
        return self.is_visible(self.ERROR_CONTAINER)
