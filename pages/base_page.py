"""
BasePage: Lớp cơ sở cung cấp các tiện ích tương tác với trình duyệt qua Selenium WebDriver.
Áp dụng mẫu thiết kế Page Object Model (POM), xử lý đồng bộ hóa (WebDriverWait)
và hỗ trợ tương tác với các ứng dụng Single Page App (SPA / React).
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, timeout)

    def open_url(self, url: str):
        """Điều hướng trình duyệt tới URL chỉ định."""
        self.driver.get(url)

    def find(self, locator):
        """Chờ phần tử hiển thị trên DOM và trả về WebElement."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Chờ tất cả phần tử hiển thị và trả về danh sách WebElement."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        """Chờ phần tử sẵn sàng click được rồi thực hiện click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except (ElementClickInterceptedException, Exception):
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator):
        """Click phần tử trực tiếp bằng JavaScript (tránh hiệu ứng animation hoặc overlay che khuất)."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text: str):
        """
        Nhập chuỗi văn bản vào input.
        Đồng thời kích hoạt sự kiện input/change tương thích với các component React.
        """
        element = self.find(locator)
        try:
            element.clear()
            element.send_keys(text)
        except Exception:
            pass

        # Đảm bảo React state cập nhật đúng kể cả khi chạy chế độ headless
        js_code = """
        let input = arguments[0];
        let val = arguments[1];
        let lastValue = input.value;
        input.value = val;
        let tracker = input._valueTracker;
        if (tracker) {
            tracker.setValue(lastValue);
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        """
        self.driver.execute_script(js_code, element, text)

    def get_text(self, locator) -> str:
        """Lấy văn bản hiển thị của phần tử."""
        element = self.find(locator)
        return element.text.strip()

    def is_visible(self, locator) -> bool:
        """Kiểm tra phần tử có đang hiển thị hay không."""
        try:
            return bool(self.find(locator).is_displayed())
        except (TimeoutException, NoSuchElementException):
            return False

    def select_dropdown_by_value(self, locator, value: str):
        """Chọn giá trị trong dropdown <select> theo attribute value."""
        element = self.find(locator)
        select = Select(element)
        select.select_by_value(value)

    def wait_for_url_contains(self, keyword: str):
        """Chờ cho đến khi URL hiện tại chứa từ khóa mong muốn."""
        return self.wait.until(EC.url_contains(keyword))

    def wait_for_url_to_be(self, expected_url: str):
        """Chờ cho đến khi URL hiện tại khớp chính xác URL mong muốn."""
        return self.wait.until(EC.url_to_be(expected_url))

    def get_current_url(self) -> str:
        """Lấy URL hiện tại của trang."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Lấy tiêu đề trang web."""
        return self.driver.title

    def save_screenshot(self, filepath: str):
        """Chụp màn hình và lưu vào tệp chỉ định."""
        self.driver.save_screenshot(filepath)
