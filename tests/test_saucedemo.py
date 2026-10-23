"""
Bộ Test Case kiểm thử tự động cho website Swag Labs (https://www.saucedemo.com/)
Bao gồm 07 Test Case chi tiết từ Đăng nhập, Tìm kiếm/Sắp xếp, Giỏ hàng, Thanh toán đến Đăng xuất.
Áp dụng mẫu thiết kế Page Object Model (POM) và Pytest Framework.
"""

import os
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo:
    @pytest.fixture(autouse=True)
    def setup_pages(self, driver):
        """Khởi tạo các đối tượng Page Object trước mỗi bài test."""
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)
        os.makedirs("screenshots", exist_ok=True)

    def test_01_valid_login(self):
        """
        TC01: Kiểm thử đăng nhập thành công với tài khoản hợp lệ
        - Bước 1: Truy cập trang chủ https://www.saucedemo.com/
        - Bước 2: Nhập username 'standard_user' và password 'secret_sauce'
        - Bước 3: Nhấn nút Login
        - Kỳ vọng: Điều hướng thành công đến trang sản phẩm (/inventory.html), tiêu đề là 'Products'.
        """
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        assert "inventory.html" in self.inventory_page.get_current_url()
        assert self.inventory_page.get_header_title() == "Products"
        self.driver.save_screenshot("screenshots/tc01_valid_login.png")

    def test_02_invalid_login_locked_user(self):
        """
        TC02: Kiểm thử đăng nhập thất bại với tài khoản bị khóa (locked_out_user)
        - Bước 1: Mở trang đăng nhập
        - Bước 2: Nhập username 'locked_out_user' và password 'secret_sauce'
        - Bước 3: Nhấn nút Login
        - Kỳ vọng: Hiển thị thông báo lỗi 'Epic sadface: Sorry, this user has been locked out.'
        """
        self.login_page.open()
        self.login_page.login("locked_out_user", "secret_sauce")

        assert self.login_page.is_error_displayed()
        assert "Sorry, this user has been locked out" in self.login_page.get_error_message()
        self.driver.save_screenshot("screenshots/tc02_locked_user.png")

    def test_03_invalid_login_wrong_credentials(self):
        """
        TC03: Kiểm thử đăng nhập thất bại khi sai mật khẩu
        - Bước 1: Mở trang đăng nhập
        - Bước 2: Nhập username 'standard_user' và mật khẩu sai 'wrong_password_123'
        - Bước 3: Nhấn nút Login
        - Kỳ vọng: Hiển thị thông báo lỗi 'Username and password do not match any user in this service'.
        """
        self.login_page.open()
        self.login_page.login("standard_user", "wrong_password_123")

        assert self.login_page.is_error_displayed()
        assert "Username and password do not match" in self.login_page.get_error_message()
        self.driver.save_screenshot("screenshots/tc03_wrong_password.png")

    def test_04_sort_products_price_low_to_high(self):
        """
        TC04: Kiểm thử chức năng sắp xếp sản phẩm theo giá tăng dần (Price: Low to High)
        - Bước 1: Đăng nhập thành công với 'standard_user'
        - Bước 2: Chọn tùy chọn sắp xếp 'Price (low to high)' (value='lohi')
        - Kỳ vọng: Danh sách giá sản phẩm được sắp xếp tăng dần chính xác.
        """
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        # Thực hiện sắp xếp
        self.inventory_page.sort_products_by("lohi")
        prices = self.inventory_page.get_product_prices()

        assert len(prices) > 0, "Danh sách sản phẩm không được rỗng"
        assert prices == sorted(prices), f"Danh sách giá chưa được sắp xếp tăng dần: {prices}"
        self.driver.save_screenshot("screenshots/tc04_sort_price_low_to_high.png")

    def test_05_add_to_cart_and_verify(self):
        """
        TC05: Kiểm thử thêm sản phẩm vào giỏ hàng và kiểm tra huy hiệu số lượng
        - Bước 1: Đăng nhập thành công
        - Bước 2: Nhấn nút 'Add to cart' cho sản phẩm 'Sauce Labs Backpack'
        - Bước 3: Kiểm tra biểu tượng giỏ hàng cập nhật số lượng = 1
        - Bước 4: Nhấn vào giỏ hàng và xác nhận sản phẩm xuất hiện trong danh sách
        - Kỳ vọng: Huy hiệu giỏ hàng hiển thị 1, trong giỏ hàng có 'Sauce Labs Backpack'.
        """
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        # Thêm sản phẩm Sauce Labs Backpack
        self.inventory_page.add_product_to_cart_by_id("add-to-cart-sauce-labs-backpack")
        assert self.inventory_page.get_cart_badge_count() == 1

        # Chuyển đến giỏ hàng để xác minh
        self.inventory_page.go_to_cart()
        assert "cart.html" in self.cart_page.get_current_url()
        items = self.cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in items
        self.driver.save_screenshot("screenshots/tc05_cart_verified.png")

    def test_06_end_to_end_checkout_success(self):
        """
        TC06: Kiểm thử luồng mua hàng hoàn chỉnh từ chọn hàng đến thanh toán thành công (E2E)
        - Bước 1: Đăng nhập bằng 'standard_user'
        - Bước 2: Thêm sản phẩm 'Sauce Labs Bike Light' vào giỏ hàng
        - Bước 3: Chuyển đến trang Giỏ hàng và nhấn Checkout
        - Bước 4: Điền thông tin giao hàng (First name, Last name, Zip code) và nhấn Continue
        - Bước 5: Kiểm tra bước xác nhận đơn hàng và nhấn Finish
        - Kỳ vọng: Hoàn tất đơn hàng với thông điệp 'Thank you for your order!'.
        """
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        # Thêm sản phẩm
        self.inventory_page.add_product_to_cart_by_id("add-to-cart-sauce-labs-bike-light")
        self.inventory_page.go_to_cart()

        # Bắt đầu checkout
        self.cart_page.click_checkout()
        assert "checkout-step-one.html" in self.checkout_page.get_current_url()

        # Nhập thông tin thanh toán
        self.checkout_page.enter_shipping_info("Nguyen", "Van A", "70000")
        self.checkout_page.click_continue()
        assert "checkout-step-two.html" in self.checkout_page.get_current_url()

        # Hoàn tất đặt hàng
        self.checkout_page.click_finish()
        assert "checkout-complete.html" in self.checkout_page.get_current_url()
        assert self.checkout_page.get_complete_header_text() == "Thank you for your order!"
        self.driver.save_screenshot("screenshots/tc06_checkout_complete.png")

    def test_07_logout_success(self):
        """
        TC07: Kiểm thử chức năng đăng xuất khỏi hệ thống
        - Bước 1: Đăng nhập thành công với 'standard_user'
        - Bước 2: Mở menu điều hướng (hamburger menu)
        - Bước 3: Nhấn nút Logout
        - Kỳ vọng: Điều hướng trở lại trang đăng nhập (URL là https://www.saucedemo.com/ và input username hiển thị).
        """
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        self.inventory_page.logout()

        assert self.login_page.get_current_url() == "https://www.saucedemo.com/"
        assert self.login_page.is_visible(self.login_page.LOGIN_BUTTON)
        self.driver.save_screenshot("screenshots/tc07_logout_success.png")
