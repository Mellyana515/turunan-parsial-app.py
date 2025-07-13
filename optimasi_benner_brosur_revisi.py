import streamlit as st
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("📦 Optimasi Produksi Banner dan Brosur")

st.markdown("Aplikasi ini menggunakan metode Linear Programming untuk mencari jumlah produksi yang memaksimalkan keuntungan berdasarkan batasan sumber daya.")

# === Sidebar: Parameter Produksi ===
st.sidebar.header("🔧 Parameter Produksi per Unit")

# Keuntungan per unit
profit_banner = st.sidebar.number_input("Keuntungan per Banner (Rp)", value=90000)
profit_brosur = st.sidebar.number_input("Keuntungan per Brosur (Rp)", value=20000)

# Waktu mesin per unit
time_banner = st.sidebar.number_input("Waktu Mesin per Banner (jam)", value=1.0)
time_brosur = st.sidebar.number_input("Waktu Mesin per Brosur (jam)", value=0.5)

# Bahan baku per unit
bahan_banner = st.sidebar.number_input("Bahan Baku per Banner (unit)", value=2.0)
bahan_brosur = st.sidebar.number_input("Bahan Baku per Brosur (unit)", value=2.0)

# Tenaga kerja per unit
tenaga_banner = st.sidebar.number_input("Tenaga Kerja per Banner (jam)", value=2.0)
tenaga_brosur = st.sidebar.number_input("Tenaga Kerja per Brosur (jam)", value=1.0)

# === Sidebar: Kapasitas Sumber Daya ===
st.sidebar.header("📊 Kapasitas Sumber Daya per Bulan")

mesin = st.sidebar.number_input("Total Kapasitas Mesin (jam)", value=150)
bahan = st.sidebar.number_input("Total Kapasitas Bahan Baku (unit)", value=200)
tenaga = st.sidebar.number_input("Total Kapasitas Tenaga Kerja (jam)", value=200)

# === Model Matematika ===
# Fungsi Objektif: Maksimalkan Z = profit_banner * x + profit_brosur * y
c = [-profit_banner, -profit_brosur]  # pakai negatif karena linprog adalah minimisasi

# Kendala:
# A_ub * [x, y] <= b_ub
A = [
    [time_banner, time_brosur],        # waktu mesin
    [bahan_banner, bahan_brosur],      # bahan baku
    [tenaga_banner, tenaga_brosur]     # tenaga kerja
]

b = [mesin, bahan, tenaga]

# Batasan x dan y ≥ 0
bounds = [(0, None), (0, None)]

# === Solusi Optimasi ===
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

st.header("📈 Hasil Optimasi Produksi")

if res.success:
    x_opt, y_opt = res.x
    keuntungan = -res.fun

    st.success("Optimasi berhasil ditemukan!")
    st.write(f"📌 Produksi optimal Banner (x): *{x_opt:.2f} unit*")
    st.write(f"📌 Produksi optimal Brosur (y): *{y_opt:.2f} unit*")
    st.write(f"💰 Total Keuntungan Maksimum: *Rp {keuntungan:,.0f}*")

    # === Visualisasi: Produksi ===
    st.subheader("📊 Visualisasi Jumlah Produksi Optimal")
    fig1, ax1 = plt.subplots()
    ax1.bar(["Banner", "Brosur"], [x_opt, y_opt], color=["skyblue", "lightgreen"])
    ax1.set_ylabel("Jumlah Produksi (unit)")
    st.pyplot(fig1)

    # === Visualisasi: Penggunaan Sumber Daya ===
    st.subheader("⚙ Pemanfaatan Sumber Daya")
    digunakan = [
        x_opt * time_banner + y_opt * time_brosur,
        x_opt * bahan_banner + y_opt * bahan_brosur,
        x_opt * tenaga_banner + y_opt * tenaga_brosur
    ]
    total = [mesin, bahan, tenaga]
    label = ["Waktu Mesin", "Bahan Baku", "Tenaga Kerja"]

    fig2, ax2 = plt.subplots()
    ax2.barh(label, total, color="gray", alpha=0.3, label="Kapasitas")
    ax2.barh(label, digunakan, color="orange", label="Terpakai")
    ax2.legend()
    st.pyplot(fig2)

else:
    st.error("Gagal menyelesaikan optimasi. Silakan cek kembali input parameter.")
