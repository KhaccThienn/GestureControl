# Hệ Thống Điều Khiển Cử Chỉ Tay

Hệ thống này cho phép người dùng điều khiển âm lượng và độ sáng màn hình của máy tính thông qua cử chỉ tay, được phát hiện bằng webcam.

## Tính năng

- **Điều khiển âm lượng**: Điều chỉnh âm lượng hệ thống bằng cách thay đổi khoảng cách giữa ngón cái và ngón út
- **Điều khiển độ sáng màn hình**: Điều chỉnh độ sáng màn hình bằng cách thay đổi khoảng cách giữa ngón cái và ngón út
- **Giao diện dòng lệnh**: Lựa chọn chế độ điều khiển thông qua menu dòng lệnh đơn giản
- **Giao diện trực quan**: Theo dõi cử chỉ tay và phản hồi trực quan thông qua cửa sổ camera

## Yêu cầu hệ thống

- Python 3.6 trở lên
- Webcam hoạt động tốt
- Các thư viện cần thiết được liệt kê trong file `requirements.txt`

## Thư viện sử dụng

| Thư viện | Mục đích sử dụng | Ghi chú |
|---------|------------------|---------|
| `numpy` | Tính toán số học, nội suy giá trị giữa khoảng cách tay và giá trị âm lượng / độ sáng. | Dùng `np.interp()` để ánh xạ khoảng cách tay sang giá trị cần điều khiển. |
| `cv2` (OpenCV) | Xử lý ảnh thời gian thực từ webcam, hiển thị giao diện người dùng và vẽ các điểm tay. | Cốt lõi cho phần xử lý hình ảnh và hiển thị giao diện. |
| `mediapipe` | Nhận diện và theo dõi bàn tay, trích xuất 21 landmark trên tay. | Cung cấp mô hình `Hands` giúp dễ dàng nhận diện cử chỉ. |
| `math.hypot` | Tính khoảng cách Euclidean giữa 2 điểm (ngón tay). | Dùng để đo khoảng cách giữa đầu ngón cái và ngón út. |
| `ctypes`, `comtypes` | Tạo đối tượng điều khiển âm lượng hệ thống bằng giao tiếp COM. | Tương tác với `IAudioEndpointVolume` trong Windows. |
| `pycaw` | Giao tiếp với hệ thống âm thanh của Windows (thông qua COM). | Điều khiển âm lượng đầu ra bằng cử chỉ. |
| `screen_brightness_control` | Điều chỉnh độ sáng màn hình. | Hỗ trợ điều khiển độ sáng với các màn hình nội bộ/laptop. |
| `os`, `sys` | Hỗ trợ thao tác hệ thống, thiết lập mã hóa UTF-8, xóa terminal,... | Hữu ích để làm sạch terminal và xử lý platform cụ thể. |

---

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python và pip
2. Cài đặt các thư viện cần thiết sử dụng file requirements.txt:

```bash
pip install -r requirements.txt
```

Nếu bạn gặp lỗi khi cài đặt các thư viện, hãy thử cài đặt từng thư viện một:

```bash
pip install numpy opencv-python mediapipe pycaw screen-brightness-control comtypes
```

## Cách sử dụng

1. Chạy chương trình:

```bash
python main.py
```

2. Trong menu dòng lệnh, chọn chế độ:
   - **1**: Điều khiển âm lượng
   - **2**: Điều khiển độ sáng
   - **0**: Thoát chương trình

3. Sau khi chọn chế độ, cửa sổ webcam sẽ hiển thị
4. Đưa bàn tay của bạn vào khung hình để bắt đầu điều khiển:
   - Thay đổi khoảng cách giữa ngón cái và ngón út để điều chỉnh giá trị
   - Khoảng cách rộng hơn = giá trị cao hơn
   - Khoảng cách hẹp hơn = giá trị thấp hơn

5. Nhấn 'q' để đóng cửa sổ webcam và quay lại menu dòng lệnh

## Cách thức hoạt động

Hệ thống sử dụng MediaPipe Hands để phát hiện và theo dõi bàn tay trong khung hình webcam. Khoảng cách giữa ngón cái và ngón út được đo lường và chuyển đổi thành giá trị điều khiển tương ứng (âm lượng hoặc độ sáng). PyCaw được sử dụng để điều khiển âm lượng hệ thống và screen_brightness_control được sử dụng để điều chỉnh độ sáng màn hình.

## Cấu trúc code

- `main.py`: File chính để chạy chương trình
- **GestureControlSystem**: Lớp chính xử lý tất cả các chức năng của hệ thống
  - **__init__()**: Khởi tạo các thành phần của hệ thống
  - **display_terminal_menu()**: Hiển thị menu dòng lệnh và xử lý lựa chọn
  - **run()**: Hàm chính điều khiển luồng chương trình
  - **run_gesture_interface()**: Khởi chạy giao diện webcam để điều khiển cử chỉ
  - **process_volume_control()**: Xử lý điều khiển âm lượng dựa trên cử chỉ tay
  - **process_brightness_control()**: Xử lý điều khiển độ sáng dựa trên cử chỉ tay
  - **cleanup()**: Giải phóng tài nguyên khi thoát chương trình

## Tùy chỉnh

Bạn có thể tùy chỉnh các thông số sau trong code:

- **min_distance** và **max_distance**: Điều chỉnh phạm vi khoảng cách tay được nhận diện
- **window_width** và **window_height**: Thay đổi kích thước cửa sổ hiển thị
- **min_detection_confidence** và **min_tracking_confidence**: Điều chỉnh độ chính xác của nhận diện bàn tay

## Nội dung file requirements.txt

File `requirements.txt` chứa danh sách các thư viện cần thiết để chạy chương trình:

```
numpy
opencv-python
mediapipe
pycaw
screen-brightness-control
comtypes
```

## Xử lý sự cố

- **Không có hình ảnh từ webcam**: Kiểm tra kết nối webcam và đảm bảo không có ứng dụng khác đang sử dụng webcam
- **Không nhận diện được bàn tay**: Đảm bảo đủ ánh sáng và bàn tay nằm hoàn toàn trong khung hình
- **Lỗi "Không tìm thấy thiết bị âm thanh"**: Kiểm tra cấu hình âm thanh của hệ thống
- **Điều khiển độ sáng không hoạt động**: Một số laptop không hỗ trợ điều khiển độ sáng bằng phần mềm
- **Lỗi khi cài đặt thư viện**: Thử cài đặt từng thư viện một và kiểm tra lỗi cụ thể
