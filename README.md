# 📈 VN30 Algorithmic Trading System
> Hệ thống phân tích kỹ thuật và giao dịch thuật toán cho thị trường phái sinh VN30

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

![Status](https://img.shields.io/badge/Trạng%20thái-Đang%20phát%20triển-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📌 Giới thiệu

**VN30 Algorithmic Trading System** là một dự án phân tích dữ liệu chứng khoán và xây dựng hệ thống giao dịch thuật toán tập trung vào nhóm **VN30F1M** (hợp đồng tương lai chỉ số VN30). Dự án kết hợp các phương pháp phân tích kỹ thuật truyền thống với các thuật toán Machine Learning hiện đại nhằm phát hiện điểm vào lệnh có xác suất thắng cao, tự động hóa quá trình đưa ra khuyến nghị giao dịch và đánh giá hiệu suất chiến lược qua backtest.

> 🎯 **Mục tiêu:** Xây dựng một pipeline hoàn chỉnh từ thu thập dữ liệu → phân tích tín hiệu → dự báo ML → báo cáo kết quả, có thể áp dụng thực tế trên thị trường phái sinh Việt Nam.

---

## ✨ Tính năng chính

### 📥 1. Thu thập & Tiền xử lý dữ liệu
- Tự động lấy dữ liệu OHLCV theo khung thời gian 5 phút từ API **vnstock3**
- Lọc thông minh: loại bỏ giờ ngoài phiên giao dịch (08:45–11:30 và 13:00–14:45)
- Loại bỏ **ngày đáo hạn phái sinh** (Thứ 5 tuần thứ 3 hàng tháng) — vùng nhiễu cực mạnh
- Xử lý outlier: lọc nến nhảy vọt bất thường (> 1%)
- Chuẩn hóa dữ liệu: tính **Log Returns** và **Z-Score** (StandardScaler)

### 📊 2. Scanner tín hiệu — Chiến lược RSI 50 + SMA 20
- Phát hiện điểm **cắt lên / cắt xuống** đường SMA 20
- Lọc xác nhận bằng chỉ báo **RSI 14** (ngưỡng trung tính 50)
- Xác nhận Volume đột biến so với trung bình 10 phiên trước
- Xuất **dashboard tương tác** bằng Plotly với bộ lọc LONG/SHORT và chức năng điều hướng nến

### 🔬 3. Scanner tín hiệu — Chiến lược SVD Confluence
- Áp dụng **Singular Value Decomposition (SVD)** trên ma trận OHLCV (window = 40 nến) để tái cấu trúc đường giá rank-2
- Phát hiện điểm **hội tụ (confluence)** khi đường SVD và EMA 20 co cụm lại (squeeze)
- Kết hợp điều kiện ATR và Volume để lọc tín hiệu chất lượng cao
- Tự động xuất báo cáo tín hiệu ra file CSV

### 🤖 4. Mô hình Machine Learning — SVD Confluence ML v3
- **Feature Engineering** từ tín hiệu hội tụ: `svd_vs_close`, `ema_vs_close`, `body`, `candle_range`, `vol_norm`, `atr_rel`
- Mô hình **Ensemble**: Random Forest (500 cây) + XGBoost, lấy trung bình xác suất
- Phân chia dữ liệu theo thời gian: 80% train / 20% predict (walk-forward)
- **Backtest thực tế**: TP = 14 điểm | SL = 7 điểm | Tối đa 100 nến chờ
- Xuất bảng kết quả đầy đủ với Win/Loss, PnL, Win Rate

### 📋 5. Báo cáo giao dịch tương tác
- Tổng hợp toàn bộ tín hiệu và kết quả thành file **HTML tương tác**
- Trực quan hóa biểu đồ nến Candlestick với overlay tín hiệu LONG/SHORT
- Thống kê hiệu suất chiến lược: Win Rate, Net Profit, số lệnh đóng

---

## 🗂️ Cấu trúc thư mục

```
VN30-Algorithmic-Trading/
│
├── 📁 data/
│   ├── 📁 raw/                          # Dữ liệu gốc — KHÔNG chỉnh sửa
│   │   ├── data.csv                     # Toàn bộ lịch sử OHLCV (~3MB, 5 phút)
│   │   └── data1thang.csv               # Dữ liệu 1 tháng gần nhất
│   │
│   └── 📁 processed/                    # Dữ liệu đã xử lý / tín hiệu đã quét
│       ├── ketqua.csv                   # Tín hiệu từ chiến lược RSI + SMA20
│       └── ket_qua_tin_hieu.csv         # Tín hiệu từ chiến lược SVD Confluence
│
├── 📁 src/                              # Mã nguồn Python chính
│   ├── config.py                        # ⚙️ Quản lý đường dẫn tập trung
│   ├── 📁 data_collection/
│   │   └── fetch_vn30_data.py           # Thu thập & tiền xử lý dữ liệu
│   ├── 📁 signals/
│   │   ├── scanner_ema20_rsi.py         # Scanner chiến lược RSI50 + SMA20
│   │   └── scanner_svd.py              # Scanner chiến lược SVD Confluence
│   └── 📁 models/
│       └── ml_recommend_v3.py          # Mô hình ML Ensemble + Backtest
│
├── 📁 notebooks/                        # Jupyter Notebooks phân tích & thử nghiệm
│   ├── VN30.ipynb                       # Khám phá dữ liệu tổng quan (EDA)
│   ├── ema20.ipynb                      # Phân tích chiến lược EMA 20
│   ├── svd.ipynb                        # Nghiên cứu thuật toán SVD
│   └── khuyennghima.ipynb              # Phát triển mô hình khuyến nghị
│
├── 📁 outputs/                          # Kết quả đầu ra
│   ├── predictions_final.csv            # Bảng dự báo ML + Win/Loss chi tiết
│   └── trading_report.html             # 📊 Báo cáo giao dịch tương tác (HTML)
│
└── README.md
```

---

## ⚙️ Cài đặt

### Yêu cầu hệ thống
- Python **3.9** trở lên
- pip hoặc conda

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/VN30-Algorithmic-Trading.git
cd VN30-Algorithmic-Trading
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
# Sử dụng venv
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

Hoặc cài trực tiếp:

```bash
pip install pandas numpy scikit-learn plotly vnstock3 xgboost openpyxl
```

<details>
<summary>📦 Danh sách thư viện chi tiết</summary>

| Thư viện | Phiên bản khuyến nghị | Mục đích |
|---|---|---|
| `pandas` | ≥ 2.0 | Xử lý & phân tích dữ liệu |
| `numpy` | ≥ 1.24 | Tính toán số học, SVD |
| `scikit-learn` | ≥ 1.3 | Random Forest, StandardScaler |
| `xgboost` | ≥ 2.0 | Gradient Boosting Classifier |
| `plotly` | ≥ 5.0 | Biểu đồ tương tác |
| `vnstock3` | mới nhất | Lấy dữ liệu thị trường VN |

</details>

---

## 🚀 Hướng dẫn sử dụng

Thực hiện theo đúng thứ tự các bước dưới đây để tạo ra báo cáo giao dịch hoàn chỉnh.

---

### Bước 1 — Thu thập dữ liệu thị trường

Script này tự động lấy dữ liệu OHLCV 5 phút của **VN30F1M** từ API, lọc giờ giao dịch, loại ngày đáo hạn và chuẩn hóa.

```bash
python src/data_collection/fetch_vn30_data.py
```

> 📂 **Output:** `data/raw/data.csv`

---

### Bước 2 — Quét tín hiệu (chọn một hoặc cả hai)

**Chiến lược A — RSI 50 + SMA 20:**
```bash
python src/signals/scanner_ema20_rsi.py
```
> 📂 **Output:** `data/processed/ketqua.csv` + Dashboard Plotly tương tác

**Chiến lược B — SVD Confluence:**
```bash
python src/signals/scanner_svd.py
```
> 📂 **Output:** `data/processed/ket_qua_tin_hieu.csv` + Biểu đồ SVD tương tác

---

### Bước 3 — Chạy mô hình Machine Learning & Backtest

```bash
python src/models/ml_recommend_v3.py
```

> 📂 **Output:** `outputs/predictions_final.csv`
> 
> 🖥️ **Console:** Bảng kết quả Win/Loss từng lệnh + thống kê chiến lược

---

### Bước 4 — Xem báo cáo giao dịch

Mở file báo cáo HTML bằng trình duyệt:

```bash
# Windows
start outputs/trading_report.html

# macOS
open outputs/trading_report.html

# Linux
xdg-open outputs/trading_report.html
```

---

### ⚡ Chạy toàn bộ pipeline (một lệnh)

```bash
python src/data_collection/fetch_vn30_data.py && \
python src/signals/scanner_ema20_rsi.py && \
python src/models/ml_recommend_v3.py
```

---

## 📊 Kết quả đạt được

Hệ thống tạo ra một **báo cáo giao dịch tương tác** (`trading_report.html`) tổng hợp toàn bộ vòng đời phân tích:

- 🗂️ **Bảng tín hiệu**: Liệt kê toàn bộ điểm vào lệnh được phát hiện, bao gồm thời gian, giá entry, hướng lệnh (LONG/SHORT), mức độ tin cậy từ mô hình ML (%)
- 📈 **Biểu đồ Candlestick**: Overlay tín hiệu trực tiếp lên đồ thị giá với marker LONG (▲ xanh) / SHORT (▼ đỏ), kèm đường SVD và EMA 20
- 🏆 **Thống kê hiệu suất (Backtest)**:
  - **Win Rate**: Tỉ lệ lệnh thắng trên tập kiểm thử 20%
  - **Net Profit**: Tổng điểm lợi nhuận ròng (TP = 14đ / SL = 7đ)
  - **Số lệnh phân tích**: Thống kê lệnh đã đóng / còn mở
- 🔍 **Bộ lọc thông minh**: Lọc bảng tín hiệu theo LONG / SHORT, điều hướng nhanh đến từng tín hiệu trên biểu đồ

---

## 🛠️ Công nghệ sử dụng

| Lĩnh vực | Công nghệ |
|---|---|
| Ngôn ngữ | Python 3.9+ |
| Xử lý dữ liệu | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Trực quan hóa | Plotly |
| Nguồn dữ liệu | vnstock3 (VCI) |
| Môi trường thử nghiệm | Jupyter Notebook |
| Phân tích nâng cao | SVD (numpy.linalg) |

---

## 📌 Lưu ý quan trọng

> ⚠️ **Tuyên bố miễn trách:** Dự án này được xây dựng hoàn toàn với mục đích **học thuật và nghiên cứu**. Các kết quả backtest và khuyến nghị giao dịch **không phải là lời khuyên đầu tư**. Hiệu suất trong quá khứ không đảm bảo kết quả trong tương lai. Người dùng tự chịu hoàn toàn trách nhiệm về các quyết định giao dịch của mình.

---

## 👤 Tác giả

**[Tên của bạn]**

[![GitHub](https://img.shields.io/badge/GitHub-@username-181717?style=flat-square&logo=github)](https://github.com/your-username)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/your-profile)

---

## 📄 Giấy phép

Dự án được phân phối theo giấy phép **MIT**. Xem thêm tại [LICENSE](LICENSE).

---

<div align="center">
  <sub>⭐ Nếu dự án này hữu ích với bạn, hãy để lại một Star trên GitHub nhé!</sub>
</div>
