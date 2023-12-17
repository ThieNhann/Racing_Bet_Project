import os
import requests

def image_to_text_online(api_key, image_path):
    # URL của OCR.space API
    ocr_api_url = "https://api.ocr.space/parse/image"

    # Thực hiện POST request đến API
    response = requests.post(
        ocr_api_url,
        files={"image": (image_path, open(image_path, "rb"))},
        data={"apikey": api_key},
    )

    # Kiểm tra xem request có thành công không
    if response.status_code == 200:
        result = response.json()
        if result["OCRExitCode"] == 1:
            return result["ParsedResults"][0]["ParsedText"]
        else:
            return f"Lỗi: {result['ErrorMessage']}"
    else:
        return f"Lỗi HTTP: {response.status_code}"

def save_text_to_file(text, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

def convert_images_in_folder(api_key, input_folder, output_folder):
    # Lấy danh sách tất cả các tệp tin hình ảnh trong thư mục đầu vào
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Lặp qua từng tệp tin hình ảnh và thực hiện chuyển đổi
    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)

        # Gọi hàm để chuyển đổi ảnh thành văn bản
        result_text = image_to_text_online(api_key, image_path)

        # Đặt đường dẫn và tên file cho kết quả
        output_file = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}.txt")

        # Gọi hàm để lưu kết quả vào file txt
        save_text_to_file(result_text, output_file)

        print(f"Kết quả từ {image_file} đã được lưu vào file: {output_file}")

# Đặt API key của bạn và đường dẫn đến thư mục chứa ảnh
api_key = "4ec40bb7f288957"  # Thay bằng API key thực tế của bạn
input_image_folder = "screenshot"  # Thay bằng đường dẫn thực tế đến thư mục ảnh
output_text_folder = "convert_result"  # Thay bằng đường dẫn thực tế đến thư mục lưu txt

# Tạo thư mục đầu ra nếu nó không tồn tại
os.makedirs(output_text_folder, exist_ok=True)

# Gọi hàm để chuyển đổi tất cả các ảnh trong thư mục
convert_images_in_folder(api_key, input_image_folder, output_text_folder)
