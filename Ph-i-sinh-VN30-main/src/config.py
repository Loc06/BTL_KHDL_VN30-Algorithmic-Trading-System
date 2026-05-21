"""
config.py — Quản lý đường dẫn tập trung cho dự án Phái sinh VN30
Mọi file .py chỉ cần import từ đây, không hardcode đường dẫn trực tiếp.
"""

from pathlib import Path

# ── Thư mục gốc dự án (tự động tính từ vị trí file này) ──────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent

# ── Dữ liệu ──────────────────────────────────────────────────────────────────
DATA_RAW_DIR       = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# File dữ liệu gốc
DATA_FULL_PATH     = DATA_RAW_DIR / "data.csv"
DATA_1THANG_PATH   = DATA_RAW_DIR / "data1thang.csv"

# File tín hiệu đã xử lý
KETQUA_EMA_PATH    = DATA_PROCESSED_DIR / "ketqua.csv"
KETQUA_SVD_PATH    = DATA_PROCESSED_DIR / "ket_qua_tin_hieu.csv"

# ── Outputs ───────────────────────────────────────────────────────────────────
OUTPUTS_DIR             = ROOT_DIR / "outputs"
PREDICTIONS_PATH        = OUTPUTS_DIR / "predictions_final.csv"
TRADING_REPORT_PATH     = OUTPUTS_DIR / "trading_report.html"

# ── Hàm tiện ích ─────────────────────────────────────────────────────────────
def ensure_dirs():
    """Tạo tất cả thư mục nếu chưa tồn tại (hữu ích khi clone repo mới)."""
    for d in [DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    print("📁 Cấu trúc thư mục dự án:")
    print(f"  ROOT          : {ROOT_DIR}")
    print(f"  data/raw      : {DATA_RAW_DIR}")
    print(f"  data/processed: {DATA_PROCESSED_DIR}")
    print(f"  outputs       : {OUTPUTS_DIR}")
