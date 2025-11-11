import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.title("🕒 Mô phỏng thời gian vỡ nợ (Time to Default Generator)")

uploaded_file = st.file_uploader("Tải file Excel doanh nghiệp (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ Đã đọc {len(df)} dòng dữ liệu")

    # Nhập thông số tùy chọn
    base_time = st.slider("Thời gian tối đa (tháng)", 12, 60, 36)
    noise = st.slider("Mức độ ngẫu nhiên (nhiễu ±)", 0, 10, 3)

    # Giả lập logic
    np.random.seed(42)
    df["time_to_default"] = (
        base_time
        - (df["X5"] * 10)
        + (df["X3"] * 5)
        + (np.random.randn(len(df)) * noise)
    )
    df["time_to_default"] = df["time_to_default"].clip(lower=1, upper=base_time)

    if "default" in df.columns:
        df.loc[df["default"] == 0, "time_to_default"] *= np.random.uniform(0.8, 1.0)
    df["time_to_default"] = df["time_to_default"].round(0)

    st.write("📊 Dữ liệu sau khi thêm cột `time_to_default`:")
    st.dataframe(df.head())

    # Tạo file để tải về
    towrite = BytesIO()
    df.to_excel(towrite, index=False, engine='xlsxwriter')
    towrite.seek(0)

    st.download_button(
        label="⬇️ Tải file Excel kết quả",
        data=towrite,
        file_name="1300dn_survival.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
