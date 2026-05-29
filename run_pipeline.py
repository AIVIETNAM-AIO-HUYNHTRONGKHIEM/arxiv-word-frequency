import subprocess
import sys
import os

def run_command(command: str, description: str) -> bool:
    """
    Ham thuc thi lenh, se tu dong dung neu co loi xay ra.
    """
    print(f"\n{'='*60}")
    print(f"Bat dau: {description}")
    print(f"Lenh dang chay: {command}")
    print(f"{'='*60}\n")
    
    try:
        # shell=True cho phep chay lenh nhu khi go truc tiep Terminal
        # check=True he thong bao loi ngay lap tuc neu lenh that bai
        subprocess.run(command, shell=True, check=True)
        print(f"\n Chay thanh cong: {description}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n Tien trinh dung khan cap!")
        print(f"Module {description} da that bai")
        return False
    
    except KeyboardInterrupt:
        print(f"\n Nguoi dung chu dong huy lenh.")
        return False

def main():
    print("🌟 TRUNG TÂM ĐIỀU KHIỂN - HỆ THỐNG PHÂN TÍCH XU HƯỚNG AI (ARXIV) 🌟")
    
    # 0. Kiểm tra an toàn trước khi cất cánh
    raw_file = "data/raw/arxiv-metadata-oai-snapshot.json"
    if not os.path.exists(raw_file):
        print(f"\n❌ LỖI CHÍNH: Không tìm thấy tệp dữ liệu gốc tại '{raw_file}'.")
        print("Vui lòng tải file từ Kaggle và đặt đúng vào thư mục cấu trúc.")
        sys.exit(1)

    # 1. GIAI ĐOẠN 1: Thu nạp & Lọc dữ liệu thô (Ingestion)
    # Nếu lệnh này False (Lỗi), sys.exit(1) sẽ ngay lập tức ngắt toàn bộ chương trình
    if not run_command("python src/ingestion.py", "Giai đoạn 1 - Xử lý Dữ liệu Thô (Ingestion)"):
        sys.exit(1)
        
    # 2. GIAI ĐOẠN 2: Tiền xử lý & Tính điểm TF-IDF (Frequency/Analytics)
    if not run_command("python src/frequency.py", "Giai đoạn 2 - Trích xuất Từ khóa & Chấm điểm TF-IDF"):
        sys.exit(1)
        
    # 3. GIAI ĐOẠN 3: Triển khai Dashboard (Visualization)
    print(f"\n{'='*60}")
    print("🎨 BẮT ĐẦU: Giai đoạn 3 - Khởi động Bảng điều khiển Giao diện Web")
    print("⏳ Trình duyệt của bạn sẽ tự động mở ra ngay sau đây...")
    print("💡 MẸO: Bấm [Ctrl + C] tại cửa sổ này bất kỳ lúc nào để tắt máy chủ web.")
    print(f"{'='*60}\n")
    
    try:
        # Streamlit là một máy chủ liên tục, nó sẽ block (chặn) chương trình tại dòng này
        # cho đến khi bạn bấm Ctrl+C để tắt
        subprocess.run("streamlit run app/dashboard.py", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Đã đóng Bảng điều khiển an toàn. Hẹn gặp lại bạn!")
    except Exception as e:
        print(f"\n❌ Lỗi khi khởi động Streamlit: {e}")

if __name__ == "__main__":
    main()
