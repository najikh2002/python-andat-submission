import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    # Gantilah dengan path dataset yang sesuai
    df = pd.read_csv("./dashboard/main_data.csv", parse_dates=[
        "order_purchase_timestamp", 
        "order_approved_at", 
        "order_delivered_carrier_date", 
        "order_delivered_customer_date", 
        "order_estimated_delivery_date"
    ])
    
    # Tambahkan kolom keterlambatan
    df["delayed"] = df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    
    # Hitung durasi pengiriman dalam hari
    df["delivery_days"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
    
    return df

df = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Pengiriman Pesanan")

# **Filter Status Pesanan**
status_list = df["order_status"].unique().tolist()
selected_status = st.multiselect("Filter Status Pesanan:", status_list, default=status_list)

# Filter data berdasarkan status
filtered_df = df[df["order_status"].isin(selected_status)]

st.subheader("Data Pesanan")
st.dataframe(filtered_df)

# **2️⃣ Visualisasi Histogram Durasi Pengiriman**
st.subheader("Distribusi Waktu Pengiriman")
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(filtered_df["delivery_days"], bins=30, kde=True, color="blue", ax=ax)
ax.set_xlabel("Hari Pengiriman")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Distribusi Waktu Pengiriman Pesanan")
st.pyplot(fig)

st.subheader("Perbandingan Estimasi vs Realisasi Pengiriman")
delayed_counts = filtered_df["delayed"].value_counts().reset_index()
delayed_counts.columns = ["Status", "Jumlah"]

fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(data=delayed_counts, x="Status", y="Jumlah", hue="Status", palette=["green", "red"], legend=False, ax=ax)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Tepat Waktu", "Terlambat"])
ax.set_xlabel("Status Pengiriman")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Perbandingan Estimasi vs Realisasi Pengiriman")
st.pyplot(fig)

st.subheader("Statistik Pengiriman")
avg_delivery_time = filtered_df["delivery_days"].mean()
late_percentage = (filtered_df["delayed"].mean()) * 100

st.metric("Rata-rata Waktu Pengiriman", f"{avg_delivery_time:.1f} hari")
st.metric("Persentase Pesanan Terlambat", f"{late_percentage:.2f}%")
