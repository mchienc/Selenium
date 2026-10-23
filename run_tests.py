"""
run_tests.py: Script tiện ích để thực thi bộ kiểm thử tự động Selenium
và mở báo cáo HTML kiểm thử sau khi hoàn thành.
"""

import sys
import os
import subprocess
import webbrowser

def main():
    print("=" * 60)
    print(" BẮT ĐẦU CHẠY BỘ KIỂM THỬ TỰ ĐỘNG VỚI SELENIUM & PYTEST")
    print("=" * 60)

    # Đảm bảo các thư mục tồn tại
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)

    # Chạy pytest thông qua module python
    args = [sys.executable, "-m", "pytest"] + sys.argv[1:]
    result = subprocess.run(args)

    report_path = os.path.abspath("reports/report.html")
    if os.path.exists(report_path):
        print("\n" + "=" * 60)
        print(f" Báo cáo HTML đã được tạo tại:")
        print(f" -> {report_path}")
        print("=" * 60)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
