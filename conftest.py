"""
conftest.py: Cấu hình Pytest Fixtures và hooks tự động chụp màn hình khi test thất bại.
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    """Thêm tham số dòng lệnh cho pytest."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Chạy trình duyệt có giao diện (headed mode), mặc định là headless",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Khởi tạo và cấu hình WebDriver trước mỗi test case.
    Tự động đóng trình duyệt sau khi test kết thúc.
    """
    is_headed = request.config.getoption("--headed")

    options = Options()
    if not is_headed:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-search-engine-choice-screen")

    # Tự động quản lý driver qua Selenium Manager hoặc ChromeDriverManager
    driver_instance = webdriver.Chrome(options=options)
    driver_instance.implicitly_wait(5)

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook kiểm tra kết quả test và chụp màn hình nếu test bị thất bại."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_instance = item.funcargs.get("driver")
        if driver_instance:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{item.name}_{timestamp}.png"
            driver_instance.save_screenshot(filename)
            print(f"\n[Screenshot captured]: {filename}")
