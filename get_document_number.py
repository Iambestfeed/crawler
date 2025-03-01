import os
import json

def extract_so_ky_hieu(downloads_folder):
    # Danh sách để lưu các số ký hiệu
    so_ky_hieu_list = []
    
    # Duyệt qua tất cả các folder con trong thư mục downloads
    for folder_name in os.listdir(downloads_folder):
        folder_path = os.path.join(downloads_folder, folder_name)
        
        # Kiểm tra nếu đây là một thư mục
        if os.path.isdir(folder_path):
            json_file_path = os.path.join(folder_path, "document_info.json")
            
            # Kiểm tra nếu file document_info.json tồn tại trong thư mục
            if os.path.exists(json_file_path):
                try:
                    # Đọc file JSON
                    with open(json_file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    # Lấy số ký hiệu từ dữ liệu JSON
                    if 'so_ky_hieu' in data:
                        so_ky_hieu = data['so_ky_hieu']
                        so_ky_hieu_list.append(so_ky_hieu)
                except Exception as e:
                    print(f"Lỗi khi đọc file {json_file_path}: {e}")
    
    # Lưu danh sách số ký hiệu vào file txt
    output_file = os.path.join(downloads_folder, "so_ky_hieu_list.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in so_ky_hieu_list:
            f.write(f"{item}\n")
    
    print(f"Đã lưu {len(so_ky_hieu_list)} số ký hiệu vào file: {output_file}")
    return so_ky_hieu_list

# Sử dụng script
if __name__ == "__main__":
    downloads_folder = input("Nhập đường dẫn đến thư mục downloads (nhấn Enter nếu là './downloads'): ")
    if not downloads_folder:
        downloads_folder = "./downloads"
    
    extract_so_ky_hieu(downloads_folder)