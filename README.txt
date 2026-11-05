# AGENT02 — Mô phỏng tác tử học tăng cường và tác tử dựa trên luật

## 1. Giới thiệu

Dự án xây dựng ứng dụng web mô phỏng và so sánh hai tác tử (agent) trong bài toán định giá và giảm giá của hai cửa hàng thương mại điện tử cạnh tranh với nhau.

Dự án thuộc môn **Intelligent System Development**, tập trung vào việc ứng dụng học tăng cường (*Reinforcement Learning*) để xây dựng tác tử có khả năng lựa chọn hành động dựa trên kinh nghiệm học được, đồng thời so sánh với tác tử sử dụng các luật cố định.

Ứng dụng sử dụng Flask để cung cấp giao diện web tương tác, cho phép người dùng thay đổi mức cầu thị trường và quan sát hành động, số lượng bán ra cùng lợi nhuận của từng tác tử qua từng bước mô phỏng.

## 2. Các tác tử

### Reinforcement Learning Agent

Sử dụng thuật toán **Q-learning** dạng bảng để học chính sách lựa chọn hành động dựa trên trạng thái hiện tại và giá trị Q đã học.

### Rule-based Agent

Sử dụng chính sách cố định được xây dựng bằng các câu lệnh `if-else`, làm đối tượng đối chiếu với tác tử học tăng cường.

### Môi trường thương mại điện tử

Môi trường mô phỏng hai cửa hàng cạnh tranh, trong đó lợi nhuận phụ thuộc vào mức cầu, hành động giảm giá, tỷ lệ chuyển đổi và số lượng khách hàng mua sản phẩm.

- **Mức cầu thấp:** 10 khách hàng mỗi lượt.
- **Mức cầu cao:** 20 khách hàng mỗi lượt.
- **Không giảm giá:** giữ nguyên giá bán.
- **Giảm giá:** áp dụng mức giảm giá được cấu hình trong chương trình.

Số lượng bán ra được lấy mẫu ngẫu nhiên theo phân phối nhị thức, phản ánh tính ngẫu nhiên của quá trình chuyển đổi khách hàng.

## 3. Chức năng

- Chạy mô phỏng từng bước thông qua giao diện web.
- Chủ động chọn mức cầu thấp hoặc cao cho mỗi lượt.
- Quan sát hành động của cả hai tác tử.
- Theo dõi số lượng bán ra, lợi nhuận và lịch sử các lượt mô phỏng.
- Xem bảng Q (*Q-table*) của tác tử học tăng cường.
- Tái sử dụng Q-table đã huấn luyện hoặc tự huấn luyện khi chưa có bảng Q hợp lệ.
- Đặt lại phiên mô phỏng để bắt đầu một lượt thử nghiệm mới.

Trong quá trình mô phỏng tương tác, chính sách RL được giữ cố định và cơ chế khám phá (*exploration*) bị tắt. Các hành động được lựa chọn dựa trên chính sách đã học, không cập nhật Q-table sau mỗi lượt tương tác.

## 4. Công nghệ sử dụng

- **Python:** xây dựng môi trường và logic mô phỏng.
- **NumPy:** tính toán số học và sinh số ngẫu nhiên.
- **Matplotlib:** trực quan hóa kết quả thí nghiệm.
- **Flask:** xây dựng web server và xử lý các yêu cầu mô phỏng.
- **HTML/CSS/JavaScript:** xây dựng giao diện người dùng.

## 5. Cấu trúc dự án

```text
AGENT02/
├── app.py
├── agent02_experiment.py
├── requirements.txt
├── README.md
├── agent02_results/
│   └── q_tables.txt
└── templates/
    ├── index.html
    └── simulation.html
```

`agent02_results/q_tables.txt` là tệp tùy chọn, chứa các giá trị Q được tạo từ quá trình huấn luyện trước đó.

## 6. Cài đặt và chạy ứng dụng

### Yêu cầu

- Python 3.10 trở lên.
- Các thư viện được liệt kê trong `requirements.txt`.

### Bước 1. Lấy mã nguồn

Sao chép hoặc tải repository về máy, sau đó mở terminal tại thư mục dự án.

### Bước 2. Chuẩn bị tệp thí nghiệm

Đặt tệp `agent02_experiment.py` gốc vào thư mục dự án.

Nếu đã chạy thí nghiệm trước đó, có thể đặt tệp Q-table tại:

```text
agent02_results/q_tables.txt
```

Nếu không có Q-table hợp lệ, ứng dụng sẽ huấn luyện tác tử RL một lần khi khởi động.

### Bước 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4. Khởi chạy ứng dụng

```bash
python app.py
```

### Bước 5. Truy cập giao diện web

Mở trình duyệt tại địa chỉ:

http://127.0.0.1:5000

## 7. Cách sử dụng

1. Truy cập trang mô phỏng.
2. Chọn mức cầu thấp hoặc cao cho lượt hiện tại.
3. Nhấn nút chạy bước tiếp theo.
4. Quan sát hành động, số lượng bán ra và lợi nhuận của hai tác tử.
5. Tiếp tục mô phỏng để theo dõi sự thay đổi của trạng thái và lịch sử.
6. Sử dụng chức năng đặt lại để bắt đầu phiên mới.

Mỗi lần thực hiện, môi trường mô phỏng một bước tương tác giữa hai tác tử. Kết quả bán hàng có tính ngẫu nhiên nên các lần chạy có thể cho kết quả khác nhau.

## 8. Phạm vi và lưu ý

Đây là mô hình mô phỏng phục vụ mục đích học tập, không phải hệ thống định giá thương mại điện tử thực tế. Các tham số về giá bán, chi phí, mức giảm giá và xác suất chuyển đổi được thiết lập để minh họa hoạt động của các tác tử.

Ứng dụng mặc định chạy trên máy cục bộ. Nếu triển khai trên môi trường công khai, cần thay khóa bí mật của Flask, cấu hình bảo mật phù hợp và sử dụng máy chủ triển khai dành cho môi trường production.
