import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.title("🕒 Mô phỏng thời gian vỡ nợ (Time to Default Generator)")

uploaded_file = st.file_uploader("📤 Tải file CSV doanh nghiệp (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"✅ Đã đọc {len(df)} dòng dữ liệu, gồm {df.shape[1]} biến")

    st.write("📄 Xem trước 5 dòng dữ liệu đầu:")
    st.dataframe(df.head())

    # Các tuỳ chọn mô phỏng
    base_time = st.slider("Thời gian tối đa (tháng)", 12, 60, 36)
    noise = st.slider("Mức độ ngẫu nhiên (nhiễu ±)", 0, 10, 3)

    np.random.seed(42)

    # Logic mô phỏng cơ bản
    if all(x in df.columns for x in ["X3", "X5"]):
        df["time_to_default"] = (
            base_time
            - (df["X5"] * 10)              # nợ cao → giảm thời gian
            + (df["X3"] * 5)               # ROA cao → sống lâu
            + (np.random.randn(len(df)) * noise)
        )
    else:
        st.warning("⚠️ Không tìm thấy X3 hoặc X5 trong dữ liệu. Hãy kiểm tra lại tên cột.")
        st.stop()

    df["time_to_default"] = df["time_to_default"].clip(lower=1, upper=base_time)

    # Nếu có cột default → điều chỉnh thêm
    if "default" in df.columns:
        df.loc[df["default"] == 0, "time_to_default"] *= np.random.uniform(0.8, 1.0)
    df["time_to_default"] = df["time_to_default"].round(0)

    st.write("📊 Dữ liệu sau khi thêm cột `time_to_default`:")
    st.dataframe(df.head())

    # Cho phép tải về file CSV mới
    towrite = BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)

    st.download_button(
        label="⬇️ Tải file CSV kết quả",
        data=towrite,
        file_name="1300dn_survival.csv",
        mime="text/csv"
    )
