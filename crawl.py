from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Thiết lập trình duyệt Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.helperApps.alwaysAsk.force", False)
firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
firefox_options.set_preference("browser.download.dir", 'D:\\crawl_\\Doc_xls')
firefox_options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
firefox_options.set_preference("pdfjs.disabled", True)
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

def crawl_documents():
    url = "https://vanban.chinhphu.vn/?pageid=41852&mode=0"
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)

    # 1️⃣ Chọn "Bộ Nội Vụ"
    select_element = wait.until(EC.presence_of_element_located((By.ID, "ctrl_191017_163_drdDocOrg")))
    select = Select(select_element)
    select.select_by_value("23")
    print("✅ Đã chọn Bộ Nội Vụ")

    # 2️⃣ Chọn hiển thị 500 kết quả
    record_select_element = wait.until(EC.presence_of_element_located((By.ID, "ctrl_191017_163_drdRecordPerPage")))
    record_select = Select(record_select_element)
    record_select.select_by_value("500")
    print("✅ Đã chọn hiển thị 500 kết quả")

    # 3️⃣ Nhấn nút tìm kiếm
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "ctrl_191017_163_btnSearch")))
    search_button.click()
    print("✅ Đã nhấn nút tìm kiếm")
    
    time.sleep(5)  # Đợi trang tải kết quả

    all_links = []
    page_count = 1

    while True:
        print(f"🔍 Đang crawl trang {page_count}...")

        # Cuộn xuống cuối trang để Selenium thấy nội dung
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Lấy danh sách văn bản
        try:
            table = driver.find_element(By.CLASS_NAME, "table.search-result")
            rows = table.find_elements(By.TAG_NAME, "tr")
        except:
            print("❌ Không tìm thấy bảng kết quả tìm kiếm!")
            break

        for row in rows:
            link_element = row.find_elements(By.TAG_NAME, "a")
            if link_element:
                link = link_element[0].get_attribute("href")
                all_links.append(link)

        # Lưu lại HTML của trang cuối cùng để debug
        with open("last_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # 1️⃣ Tìm `Page$k+1` trước
        try:
            next_page = driver.find_element(By.XPATH, f"//td/a[contains(@href, \"Page${page_count + 1}\")]")
            print(f"✅ Nhấn vào trang {page_count + 1}")
            driver.execute_script("arguments[0].click();", next_page)
            page_count += 1
            time.sleep(3)
            continue  # Nếu tìm thấy `Page$k+1`, tiếp tục vòng lặp
        except:
            next_page = None

        # 2️⃣ Nếu không tìm thấy `Page$k+1`, thử mở rộng danh sách trang bằng cách bấm "..."
        try:
            expand_page = driver.find_element(By.XPATH, "//td/a[contains(text(), '...')]")
            print("🔄 Mở rộng danh sách trang bằng cách nhấn '...'")
            driver.execute_script("arguments[0].click();", expand_page)
            time.sleep(3)

            # Sau khi mở rộng, kiểm tra lại `Page$k+1`
            try:
                next_page = driver.find_element(By.XPATH, f"//td/a[contains(@href, \"Page${page_count + 1}\")]")
                print(f"✅ Nhấn vào trang {page_count + 1} sau khi mở rộng")
                driver.execute_script("arguments[0].click();", next_page)
                page_count += 1
                time.sleep(3)
                continue
            except:
                print("❌ Không tìm thấy trang mới sau khi mở rộng.")
                break
        except:
            print("✅ Không còn trang tiếp theo. Kết thúc crawl.")
            break

    driver.quit()

    # Lưu danh sách văn bản vào file
    with open("documents.txt", "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

    print(f"📜 Tổng số văn bản lấy được: {len(all_links)}")
    return all_links

# Chạy crawl
document_links = crawl_documents()
