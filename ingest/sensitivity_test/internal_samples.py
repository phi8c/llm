# experiments/sensitivity_test/internal_samples_hr_policy.py

SAMPLES = [
    # ===== ĐIỀU 1 – THỜI GIAN LÀM VIỆC =====
    {
        "text": """Thời gian làm việc từ thứ Hai đến thứ Sáu, giờ làm việc 08:30 – 17:30.""",
        "owner_role": "hr",
        "expected_internal": False,
    },

    {
        "text": """Nhân viên được phép đi muộn/về sớm tối đa 60 phút/tháng mà không bị trừ lương.""",
        "owner_role": "hr",
        "expected_internal": True,  # liên quan trực tiếp tới lương
    },

    {
        "text": """Nhân viên quên chấm công quá 3 lần/tháng phải làm giải trình và có xác nhận của Quản lý.""",
        "owner_role": "hr",
        "expected_internal": True,  # quy trình xử lý nội bộ
    },

    # ===== ĐIỀU 2 – DRESS CODE =====
    {
        "text": """Nhân viên phải mặc trang phục lịch sự, gọn gàng, đeo thẻ tên khi làm việc.""",
        "owner_role": "hr",
        "expected_internal": False,
    },

    # ===== ĐIỀU 3 – NGHỈ PHÉP =====
    {
        "text": """Nhân viên chính thức được hưởng 12 ngày phép năm hưởng nguyên lương.""",
        "owner_role": "hr",
        "expected_internal": False,  # quyền lợi chung
    },

    {
        "text": """Phép năm không sử dụng hết được bảo lưu tối đa 5 ngày sang Quý 1 năm sau.""",
        "owner_role": "hr",
        "expected_internal": True,  # quy định nội bộ chi tiết
    },

    # ===== ĐIỀU 4 – THAI SẢN =====
    {
        "text": """Nhân viên nữ được nghỉ thai sản 06 tháng theo quy định.""",
        "owner_role": "hr",
        "expected_internal": False,
    },

    {
        "text": """Trợ cấp thai sản hưởng 100% bình quân tiền lương đóng BHXH của 06 tháng liền kề.""",
        "owner_role": "hr",
        "expected_internal": True,  # tiền + cách tính
    },

    {
        "text": """Công ty hỗ trợ thêm 01 tháng lương cơ bản như một khoản chúc mừng sinh con.""",
        "owner_role": "hr",
        "expected_internal": True,  # tiền cụ thể
    },

    # ===== ĐIỀU 5 – LƯƠNG THƯỞNG =====
    {
        "text": """Lương được thanh toán vào ngày 05 hàng tháng qua tài khoản ngân hàng.""",
        "owner_role": "hr",
        "expected_internal": True,
    },

    {
        "text": """Lương làm thêm giờ ngày thường: 150%, ngày nghỉ tuần: 200%, ngày lễ: 300%.""",
        "owner_role": "hr",
        "expected_internal": True,
    },

    {
        "text": """Phụ cấp ăn trưa 730.000 VNĐ/tháng, phụ cấp gửi xe 150.000 VNĐ/tháng.""",
        "owner_role": "hr",
        "expected_internal": True,
    },

    # ===== JD – TUYỂN DỤNG =====
    {
        "text": """Tiếp nhận nhu cầu tuyển dụng, đăng tin và sàng lọc hồ sơ ứng viên.""",
        "owner_role": "hr",
        "expected_internal": False,
    },

    {
        "text": """Gửi Offer Letter và đàm phán lương với ứng viên.""",
        "owner_role": "hr",
        "expected_internal": True,
    },

    # ===== JD – HR MANAGER =====
    {
        "text": """Tham mưu cho Ban Giám đốc về chiến lược phát triển nguồn nhân lực.""",
        "owner_role": "hr",
        "expected_internal": False,
    },

    {
        "text": """Quản lý, đánh giá hiệu quả làm việc của nhân viên phòng HR.""",
        "owner_role": "hr",
        "expected_internal": True,
    },
]
