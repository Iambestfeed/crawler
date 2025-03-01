import os
import json
import requests
from bs4 import BeautifulSoup

def safe_get_text(element):
    return element.text.strip() if element else "N/A"

def fetch_document_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Giả lập trình duyệt
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    document = {}
    document['title'] = safe_get_text(soup.select_one('span[id^="ctrl_"][id$="_lb_noidung"]'))
    document['so_ky_hieu'] = safe_get_text(soup.select_one('td.col1:contains("Số ký hiệu") + td'))
    document['ngay_ban_hanh'] = safe_get_text(soup.select_one('td.col1:contains("Ngày ban hành") + td'))
    document['ngay_co_hieu_luc'] = safe_get_text(soup.select_one('td.col1:contains("Ngày có hiệu lực") + td'))
    document['loai_van_ban'] = safe_get_text(soup.select_one('td.col1:contains("Loại văn bản") + td'))
    document['co_quan_ban_hanh'] = safe_get_text(soup.select_one('td.col1:contains("Cơ quan ban hành") + td'))
    document['nguoi_ky'] = safe_get_text(soup.select_one('td.col1:contains("Người ký") + td'))
    document['trich_yeu'] = safe_get_text(soup.select_one('td.col1:contains("Trích yếu") + td'))
    
    pdf_links = []
    for a_tag in soup.select('td:contains("Tài liệu đính kèm") a.view-file'):
        if a_tag and 'href' in a_tag.attrs:
            pdf_url = a_tag['href']
            if not pdf_url.startswith('http'):
                pdf_url = f"https://datafiles.chinhphu.vn/{pdf_url}"  # Thêm domain nếu thiếu
            pdf_links.append((safe_get_text(a_tag), pdf_url))
    
    document['pdf_files'] = pdf_links
    return document

def download_pdf(pdf_url, save_dir, doc_id, source_url):
    os.makedirs(save_dir, exist_ok=True)
    filename = pdf_url.split('/')[-1]
    save_path = os.path.join(save_dir, filename)
    
    if os.path.exists(save_path):
        print(f"Skipping already downloaded: {filename}")
        return
    
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename}")
        with open("debug_failed_downloads.txt", "a") as debug_file:
            debug_file.write(f"Document ID: {doc_id}, Source URL: {source_url}, PDF URL: {pdf_url}\n")

def save_document_info(document_info, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    json_path = os.path.join(save_dir, 'document_info.json')
    
    if os.path.exists(json_path):
        print(f"Skipping already saved document info: {json_path}")
        return
    
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(document_info, json_file, ensure_ascii=False, indent=4)
    print(f"Saved document info: {json_path}")

def load_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def main(file_path):
    urls = load_urls_from_file(file_path)
    for url in urls:
        doc_id = url.split('=')[-1]
        save_dir = os.path.join('downloads', doc_id)
        
        document_info = fetch_document_info(url)
        if document_info:
            save_document_info(document_info, save_dir)
            for filename, pdf_url in document_info['pdf_files']:
                download_pdf(pdf_url, save_dir, doc_id, url)

if __name__ == "__main__":
    file_path = "documents.txt"
    main(file_path)
