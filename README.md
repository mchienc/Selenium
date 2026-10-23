# BÁO CÁO THỰC HÀNH KIỂM THỬ TỰ ĐỘNG VỚI SELENIUM WEBDRIVER

---

## THÔNG TIN SINH VIÊN & BÀI NỘP
- **Môn học:** Đảm bảo chất lượng & Kiểm thử phần mềm (Software Quality Assurance & Testing)
- **Họ và tên sinh viên:** *Nguyễn Văn A (Sinh viên cập nhật)*
- **Mã số sinh viên (MSSV):** *2021xxxx (Sinh viên cập nhật)*
- **Lớp:** *CNTT (Sinh viên cập nhật)*
- **Website mục tiêu kiểm thử:** [Swag Labs (SauceDemo)](https://www.saucedemo.com/)
- **GitHub Repository:** [https://github.com/mchienc/Selenium](https://github.com/mchienc/Selenium)
- **Link Google Sheet nộp bài:** [Google Sheet Nộp Bài Test](https://docs.google.com/spreadsheets/d/1GyPWJ9lbhoWOO_bew4715lVoxttf727u7ihrD4hobEM/edit?gid=0#gid=0)

---

## 1. TỔNG QUAN VỀ CÔNG CỤ SELENIUM WEBDRIVER

### 1.1. Selenium là gì?
**Selenium** là một bộ công cụ mã nguồn mở hàng đầu thế giới được sử dụng để tự động hóa các thao tác trên trình duyệt web (Web Browser Automation). Selenium hỗ trợ mô phỏng các hành vi thực tế của người dùng như nhấp chuột (click), nhập liệu (type/send_keys), điều hướng trang, chọn dropdown, xác thực thông tin và kiểm tra giao diện người dùng.

Bộ công cụ Selenium bao gồm:
1. **Selenium WebDriver:** Thư viện lập trình mạnh mẽ nhất của Selenium, giao tiếp trực tiếp với các trình duyệt thông qua driver native (Chromedriver, Geckodriver, Edgedriver) theo chuẩn **W3C WebDriver Specification**.
2. **Selenium IDE:** Extension trên Chrome/Firefox hỗ trợ ghi lại (Record) và phát lại (Playback) các thao tác kiểm thử nhanh.
3. **Selenium Grid:** Giải pháp hỗ trợ chạy các bài kiểm thử song song (Parallel execution) trên nhiều máy, hệ điều hành và trình duyệt khác nhau.

### 1.2. Ưu điểm nổi bật của Selenium WebDriver
- **Đa nền tảng và đa ngôn ngữ:** Hỗ trợ Python, Java, C#, JavaScript, Ruby trên Windows, macOS, Linux.
- **Hỗ trợ đầy đủ các trình duyệt phổ biến:** Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari.
- **Tích hợp linh hoạt với Test Frameworks:** Dễ dàng kết hợp với **Pytest**, **Unittest**, **TestNG**, **JUnit**, các công cụ CI/CD (GitHub Actions, Jenkins).
- **Cộng đồng hỗ trợ lớn:** Tài liệu phong phú, giải quyết lỗi nhanh chóng.

### 1.3. Tài liệu & Video tự học tham khảo
- **Tài liệu chính thức (Official Docs):** [Selenium Documentation](https://www.selenium.dev/documentation/)
- **Kho lưu trữ W3C WebDriver:** [W3C WebDriver Recommendation](https://www.w3.org/TR/webdriver/)
- **Video hướng dẫn tự học Selenium Python:**
  - *Selenium WebDriver with Python Tutorial* - freeCodeCamp.org
  - *Selenium Python Automation Testing from Scratch* - Tech With Tim
  - Khóa học thực hành Selenium trên edX & Coursera

---

## 2. KIẾN TRÚC DỰ ÁN & MẪU THIẾT KẾ PAGE OBJECT MODEL (POM)

Dự án áp dụng mô hình thiết kế **Page Object Model (POM)** – tiêu chuẩn vàng trong ngành kiểm thử phần mềm tự động:
- **Tách biệt hoàn toàn logic kiểm thử (Tests) và logic giao diện (Pages):** Mỗi trang web được biểu diễn bởi một lớp (Class) trong thư mục `pages/`. Mọi locator (ID, CSS selector, XPath) và hành vi (actions) đều được đóng gói bên trong Class đó.
- **Dễ bảo trì và mở rộng (High Maintainability):** Khi UI của website thay đổi, chúng ta chỉ cần cập nhật locator trong file Page tương ứng mà không phải sửa đổi kịch bản trong các file Test.
- **Tái sử dụng mã nguồn (Reusability):** Các hàm đăng nhập, điều hướng, thêm sản phẩm được tái sử dụng xuyên suốt bộ kiểm thử.
- **Cơ chế chờ thông minh (Explicit Waits):** Sử dụng `WebDriverWait` và `expected_conditions` thay cho `sleep()`, giúp kiểm thử chạy nhanh, ổn định và không bị gián đoạn do độ trễ mạng.

```
                           +---------------------------+
                           |  tests/test_saucedemo.py  |
                           +-------------+-------------+
                                         |
                                         v
    +------------------------------------+------------------------------------+
    |                    pages/ (Page Object Model)                           |
    |                                                                         |
    |  +-------------------+  +---------------------+  +-------------------+  |
    |  |     LoginPage     |  |    InventoryPage    |  |     CartPage      |  |
    |  +---------+---------+  +----------+----------+  +---------+---------+  |
    |            |                       |                       |            |
    |            +-----------------------+-----------------------+            |
    |                                    |                                    |
    |                                    v                                    |
    |                          +-------------------+                          |
    |                          |     BasePage      |                          |
    |                          +---------+---------+                          |
    +------------------------------------+------------------------------------+
                                         |
                                         v
                         +-------------------------------+
                         |   Selenium WebDriver Engine   |
                         +---------------+---------------+
                                         |
                                         v
                       +-----------------------------------+
                       | Target Website: www.saucedemo.com |
                       +-----------------------------------+
```

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```
selemium/
├── pages/                          # Các lớp Page Object đóng gói phần tử & hành động UI
│   ├── __init__.py
│   ├── base_page.py                # Lớp cơ sở (find, click, enter_text, wait, JS click)
│   ├── login_page.py               # Trang đăng nhập (locators, login action, get error)
│   ├── inventory_page.py           # Trang danh sách sản phẩm (sắp xếp, lọc, thêm giỏ, logout)
│   ├── cart_page.py                # Trang giỏ hàng (kiểm tra sản phẩm, checkout)
│   └── checkout_page.py            # Trang thanh toán (thông tin giao hàng, xác nhận đặt hàng)
├── tests/                          # Thư mục kịch bản kiểm thử
│   ├── __init__.py
│   └── test_saucedemo.py           # Bộ 07 test cases chi tiết thực hiện với Pytest
├── reports/                        # Báo cáo kết quả kiểm thử tự động
│   └── report.html                 # Báo cáo HTML trực quan, chi tiết từng bài test
├── screenshots/                    # Ảnh chụp màn hình minh chứng kết quả kiểm thử
│   ├── tc01_valid_login.png
│   ├── tc02_locked_user.png
│   ├── tc03_wrong_password.png
│   ├── tc04_sort_price_low_to_high.png
│   ├── tc05_cart_verified.png
│   ├── tc06_checkout_complete.png
│   └── tc07_logout_success.png
├── conftest.py                     # Cấu hình Pytest Fixtures, Driver Setup & Hook chụp ảnh
├── pytest.ini                      # Tệp cấu hình tham số mặc định cho Pytest
├── requirements.txt                # Danh sách thư viện phụ thuộc (Selenium, Pytest,...)
├── run_tests.py                    # Script tiện ích một lệnh để chạy toàn bộ kiểm thử
└── README.md                       # Báo cáo tổng hợp dự án kiểm thử
```

---

## 4. DANH SÁCH & ĐẶC TẢ CHI TIẾT 07 TEST CASES KIỂM THỬ TỰ ĐỘNG

Dự án xây dựng **07 Test Cases** hoàn chỉnh (vượt yêu cầu tối thiểu 05 test cases của đề bài):

| STT | Mã TC | Tên Test Case | Mục tiêu kiểm thử | Trạng thái |
|:---:|:---:|:---|:---|:---:|
| 1 | **TC01** | `test_01_valid_login` | Kiểm thử đăng nhập thành công với tài khoản chuẩn | **PASSED** |
| 2 | **TC02** | `test_02_invalid_login_locked_user` | Kiểm thử thông báo lỗi khi đăng nhập tài khoản bị khóa | **PASSED** |
| 3 | **TC03** | `test_03_invalid_login_wrong_credentials` | Kiểm thử thông báo lỗi khi nhập sai mật khẩu | **PASSED** |
| 4 | **TC04** | `test_04_sort_products_price_low_to_high` | Kiểm thử chức năng sắp xếp sản phẩm theo giá tăng dần | **PASSED** |
| 5 | **TC05** | `test_05_add_to_cart_and_verify` | Kiểm thử thêm sản phẩm vào giỏ hàng và huy hiệu đếm | **PASSED** |
| 6 | **TC06** | `test_06_end_to_end_checkout_success` | Kiểm thử luồng mua hàng và thanh toán trọn vẹn (End-to-End) | **PASSED** |
| 7 | **TC07** | `test_07_logout_success` | Kiểm thử chức năng đăng xuất khỏi hệ thống an toàn | **PASSED** |

---

### Bảng đặc tả chi tiết từng Test Case:

#### 1. TC01: Đăng nhập thành công với tài khoản hợp lệ
- **Mã kịch bản:** `test_01_valid_login`
- **Mục đích:** Xác thực người dùng có thể đăng nhập thành công vào hệ thống bằng thông tin đăng nhập chính xác.
- **Tiền điều kiện (Preconditions):** Trình duyệt mở và điều hướng tới `https://www.saucedemo.com/`.
- **Dữ liệu kiểm thử (Test Data):**
  - Username: `standard_user`
  - Password: `secret_sauce`
- **Các bước thực hiện (Steps):**
  1. Nhập username vào ô `#user-name`.
  2. Nhập password vào ô `#password`.
  3. Nhấp nút `#login-button`.
- **Kết quả mong đợi (Expected):** Điều hướng tới trang sản phẩm `https://www.saucedemo.com/inventory.html`, tiêu đề trang hiển thị `Products`.
- **Kết quả thực tế (Actual):** Đăng nhập thành công, URL đúng và header hiển thị `Products`.

---

#### 2. TC02: Đăng nhập thất bại với tài khoản bị khóa
- **Mã kịch bản:** `test_02_invalid_login_locked_user`
- **Mục đích:** Kiểm tra thông báo lỗi khi người dùng bị khóa cố gắng đăng nhập vào hệ thống.
- **Tiền điều kiện:** Mở trang đăng nhập.
- **Dữ liệu kiểm thử:**
  - Username: `locked_out_user`
  - Password: `secret_sauce`
- **Các bước thực hiện:**
  1. Nhập username `locked_out_user`.
  2. Nhập password `secret_sauce`.
  3. Nhấp nút Login.
- **Kết quả mong đợi:** Người dùng không được chuyển trang; hiển thị thông báo lỗi: `Epic sadface: Sorry, this user has been locked out.`.
- **Kết quả thực tế:** Thông báo lỗi hiển thị chính xác như kỳ vọng.

---

#### 3. TC03: Đăng nhập thất bại khi sai thông tin xác thực
- **Mã kịch bản:** `test_03_invalid_login_wrong_credentials`
- **Mục đích:** Xác thực hệ thống từ chối đăng nhập khi người dùng nhập sai mật khẩu.
- **Tiền điều kiện:** Mở trang đăng nhập.
- **Dữ liệu kiểm thử:**
  - Username: `standard_user`
  - Password: `wrong_password_123`
- **Các bước thực hiện:**
  1. Nhập username `standard_user`.
  2. Nhập password sai `wrong_password_123`.
  3. Nhấp nút Login.
- **Kết quả mong đợi:** Hiển thị thông báo lỗi: `Epic sadface: Username and password do not match any user in this service`.
- **Kết quả thực tế:** Hiển thị thông báo lỗi bảo mật chính xác.

---

#### 4. TC04: Sắp xếp danh sách sản phẩm theo giá tăng dần
- **Mã kịch bản:** `test_04_sort_products_price_low_to_high`
- **Mục đích:** Kiểm tra tính năng lọc/sắp xếp sản phẩm theo tiêu chí giá từ thấp đến cao (Price: low to high).
- **Tiền điều kiện:** Đã đăng nhập vào trang sản phẩm `/inventory.html`.
- **Dữ liệu kiểm thử:** Chọn option `lohi` trong dropdown sắp xếp.
- **Các bước thực hiện:**
  1. Xác định dropdown `select.product_sort_container`.
  2. Chọn giá trị `lohi`.
  3. Thu thập danh sách giá hiển thị của toàn bộ các sản phẩm.
- **Kết quả mong đợi:** Danh sách giá hiển thị theo thứ tự tăng dần thỏa mãn điều kiện `prices == sorted(prices)`.
- **Kết quả thực tế:** Các mức giá hiển thị ($7.99, $9.99, $15.99, $15.99, $29.99, $49.99) được sắp xếp chuẩn xác 100%.

---

#### 5. TC05: Thêm sản phẩm vào giỏ hàng & kiểm tra huy hiệu số lượng
- **Mã kịch bản:** `test_05_add_to_cart_and_verify`
- **Mục đích:** Xác thực người dùng có thể thêm sản phẩm vào giỏ hàng và huy hiệu biểu tượng giỏ hàng cập nhật đúng số lượng.
- **Tiền điều kiện:** Đã đăng nhập vào trang danh sách sản phẩm.
- **Dữ liệu kiểm thử:** Sản phẩm `Sauce Labs Backpack`.
- **Các bước thực hiện:**
  1. Nhấn nút `#add-to-cart-sauce-labs-backpack`.
  2. Kiểm tra số lượng trên huy hiệu `.shopping_cart_badge`.
  3. Nhấp vào icon giỏ hàng để chuyển trang `/cart.html`.
  4. Kiểm tra tên sản phẩm trong danh sách giỏ hàng.
- **Kết quả mong đợi:** Huy hiệu hiển thị `1`, trong giỏ hàng có chứa sản phẩm `Sauce Labs Backpack`.
- **Kết quả thực tế:** Số lượng cập nhật chính xác và sản phẩm hiện diện trong giỏ hàng.

---

#### 6. TC06: Quy trình mua hàng & thanh toán End-to-End (E2E)
- **Mã kịch bản:** `test_06_end_to_end_checkout_success`
- **Mục đích:** Kiểm thử toàn diện quy trình mua hàng từ khi chọn sản phẩm, vào giỏ hàng, nhập thông tin giao hàng đến khi hoàn tất đơn hàng.
- **Tiền điều kiện:** Đã đăng nhập vào hệ thống.
- **Dữ liệu kiểm thử:**
  - Sản phẩm: `Sauce Labs Bike Light`
  - Thông tin nhận hàng: First Name: `Nguyen`, Last Name: `Van A`, Postal Code: `70000`
- **Các bước thực hiện:**
  1. Thêm `Sauce Labs Bike Light` vào giỏ hàng.
  2. Mở trang Giỏ hàng và nhấp nút `Checkout`.
  3. Nhập First Name, Last Name, Postal Code vào form bước 1 và nhấn `Continue`.
  4. Chuyển sang bước tổng quan đơn hàng (Step 2) và kiểm tra thông tin, sau đó nhấn `Finish`.
  5. Kiểm tra thông điệp xác nhận tại trang `/checkout-complete.html`.
- **Kết quả mong đợi:** Đơn hàng được tạo thành công, hiển thị dòng chữ: `Thank you for your order!`.
- **Kết quả thực tế:** Quy trình hoàn tất trơn tru, tiêu đề xác nhận hiển thị chính xác.

---

#### 7. TC07: Đăng xuất khỏi hệ thống thành công
- **Mã kịch bản:** `test_07_logout_success`
- **Mục đích:** Xác thực phiên làm việc của người dùng được hủy bỏ an toàn khi chọn Đăng xuất.
- **Tiền điều kiện:** Người dùng đang ở trạng thái đã đăng nhập.
- **Các bước thực hiện:**
  1. Nhấp vào nút mở menu thanh điều hướng `#react-burger-menu-btn`.
  2. Nhấp vào liên kết `#logout_sidebar_link`.
- **Kết quả mong đợi:** Trình duyệt điều hướng quay lại trang chủ `https://www.saucedemo.com/`, form đăng nhập hiển thị sẵn sàng.
- **Kết quả thực tế:** Trình duyệt chuyển về đúng trang Login, nút Đăng nhập hiển thị bình thường.

---

## 5. HƯỚNG DẪN CÀI ĐẶT & CHẠY KIỂM THỬ

### 5.1. Yêu cầu môi trường
- Hệ điều hành: Windows 10/11, macOS hoặc Linux.
- Đã cài đặt **Python 3.10+** (Kiểm tra bằng: `python --version`).
- Trình duyệt **Google Chrome** bản mới nhất.

### 5.2. Các bước cài đặt thư viện
Mở Terminal hoặc Command Prompt tại thư mục dự án và chạy lệnh:
```bash
pip install -r requirements.txt
```

### 5.3. Các phương thức thực thi kiểm thử

#### Cách 1: Chạy toàn bộ kiểm thử ở chế độ ngầm định (Headless - khuyến nghị)
```bash
python -m pytest
```
*Lưu ý: Chế độ Headless giúp kiểm thử chạy cực nhanh trong nền mà không chiếm dụng màn hình làm việc.*

#### Cách 2: Chạy kiểm thử có hiển thị giao diện trình duyệt (Headed mode)
```bash
python -m pytest --headed
```

#### Cách 3: Chạy thông qua script tiện ích `run_tests.py`
```bash
python run_tests.py
```

#### Cách 4: Chạy riêng một test case cụ thể (Ví dụ chạy TC01)
```bash
python -m pytest tests/test_saucedemo.py -k "test_01_valid_login"
```

---

## 6. KẾT QUẢ THỰC THI & BÁO CÁO KIỂM THỬ (TEST EXECUTION REPORT)

### 6.1. Tổng kết kết quả chạy Test
```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.7.0
rootdir: D:\selemium
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.12.1, html-4.2.0, metadata-3.1.1
collected 7 items

tests/test_saucedemo.py::TestSauceDemo::test_01_valid_login PASSED       [ 14%]
tests/test_saucedemo.py::TestSauceDemo::test_02_invalid_login_locked_user PASSED [ 28%]
tests/test_saucedemo.py::TestSauceDemo::test_03_invalid_login_wrong_credentials PASSED [ 42%]
tests/test_saucedemo.py::TestSauceDemo::test_04_sort_products_price_low_to_high PASSED [ 57%]
tests/test_saucedemo.py::TestSauceDemo::test_05_add_to_cart_and_verify PASSED   [ 71%]
tests/test_saucedemo.py::TestSauceDemo::test_06_end_to_end_checkout_success PASSED [ 85%]
tests/test_saucedemo.py::TestSauceDemo::test_07_logout_success PASSED           [100%]

------- Generated html report: file:///D:/selemium/reports/report.html --------
============================= 7 passed in 30.57s ==============================
```

- **Tổng số test cases:** 7
- **Số test case đạt (Passed):** 7 (100%)
- **Số test case thất bại (Failed):** 0 (0%)
- **Thời gian thực thi trung bình:** ~30 giây cho toàn bộ 7 kịch bản end-to-end.
- **Tệp báo cáo trực quan:** Mở tệp `reports/report.html` trên bất kỳ trình duyệt nào để xem thống kê trực quan.

### 6.2. Hình ảnh minh chứng thực thi (Evidence Screenshots)
Các ảnh chụp màn hình minh chứng được tự động lưu trong thư mục `screenshots/`:
- `screenshots/tc01_valid_login.png`: Giao diện sau khi đăng nhập thành công.
- `screenshots/tc02_locked_user.png`: Thông báo lỗi tài khoản bị khóa.
- `screenshots/tc03_wrong_password.png`: Thông báo lỗi mật khẩu không trùng khớp.
- `screenshots/tc04_sort_price_low_to_high.png`: Danh sách sản phẩm được sắp xếp tăng dần theo giá.
- `screenshots/tc05_cart_verified.png`: Sản phẩm nằm trong giỏ hàng và huy hiệu số lượng.
- `screenshots/tc06_checkout_complete.png`: Thông báo đặt hàng thành công (`Thank you for your order!`).
- `screenshots/tc07_logout_success.png`: Điều hướng trở về trang đăng nhập sau khi đăng xuất.

---

## 7. HƯỚNG DẪN ĐẨY DỰ ÁN LÊN GITHUB & NỘP BÀI

### 7.1. Tạo mới và đẩy mã nguồn lên GitHub Repo
1. Mở trình duyệt, truy cập [GitHub](https://github.com/) và tạo một Repository mới (ví dụ: `selenium-automation-testing`).
2. Tại máy cá nhân, mở terminal trong thư mục dự án và thực hiện các lệnh sau:

```bash
# Khởi tạo git repository tại thư mục dự án
git init

# Thêm tất cả các file mã nguồn vào staging
git add .

# Tạo commit đầu tiên
git commit -m "feat: complete selenium automated testing with 7 test cases and POM architecture"

# Đổi nhánh mặc định sang main
git branch -M main

# Liên kết với repo GitHub của bạn (thay YOUR_USERNAME và REPO_NAME tương ứng)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Đẩy code lên GitHub
git push -u origin main
```

### 7.2. Nộp bài trên Google Sheet
1. Mở đường link Google Sheet: [Link Google Sheet](https://docs.google.com/spreadsheets/d/1GyPWJ9lbhoWOO_bew4715lVoxttf727u7ihrD4hobEM/edit?gid=0#gid=0).
2. Tìm đến đúng dòng thông tin của bạn (cùng sheet đã nộp bài Postman trước đó).
3. Dán link GitHub Repository của bạn vào cột nộp bài Selenium.
