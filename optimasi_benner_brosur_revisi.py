import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(layout="centered")
st.title("📦 Optimasi Produksi Banner dan Brosur (Input Manual + Jumlah Karyawan)")

st.markdown("Masukkan data produksi, sumber daya, dan jumlah karyawan untuk menentukan kombinasi produksi optimal dengan metode Linear Programming.")

# ------------------------ INPUT ------------------------
st.sidebar.header("📥 Parameter Produksi")

# Keuntungan per unit
profit_x = st.sidebar.number_input("Keuntungan per unit Banner (Rp)", value=90000)
profit_y = st.sidebar.number_input("Keuntungan per unit Brosur (Rp)", value=20000)

# Biaya variabel
cost_x = st.sidebar.number_input("Biaya per unit Banner (Rp)", value=35000)
cost_y = st.sidebar.number_input("Biaya per unit Brosur (Rp)", value=10000)

# Biaya tetap mingguan
fixed_cost = st.sidebar.number_input("Biaya Tetap Mingguan (Rp)", value=675000)

# Jumlah karyawan & kapasitas kerja
jumlah_karyawan = st.sidebar.number_input("Jumlah Karyawan", min_value=1, value=1)
kapasitas_per_karyawan = st.sidebar.number_input("Jam kerja per karyawan per bulan", value=200)
total_tenaga_kerja = jumlah_karyawan * kapasitas_per_karyawan

# Kapasitas lain
kap_mesin = st.sidebar.number_input("Kapasitas Mesin (jam/bulan)", value=150)
kap_bahan = st.sidebar.number_input("Kapasitas Bahan Baku (unit/bulan)", value=200)

# Konsumsi per unit
m_x = st.sidebar.number_input("Jam Mesin per Banner", value=3.0)
m_y = st.sidebar.number_input("Jam Mesin per Brosur", value=0.5)

b_x = st.sidebar.number_input("Bahan Baku per Banner", value=2.0)
b_y = st.sidebar.number_input("Bahan Baku per Brosur", value=2.0)

t_x = st.sidebar.number_input("Jam Tenaga Kerja per Banner", value=2.0)
t_y = st.sidebar.number_input("Jam Tenaga Kerja per Brosur", value=1.0)

# ------------------------ LINEAR PROGRAMMING ------------------------
c = [-profit_x, -profit_y]
A = [
    [m_x, m_y],       # Mesin
    [b_x, b_y],       # Bahan
    [t_x, t_y]        # Tenaga kerja
]
b = [kap_mesin, kap_bahan, total_tenaga_kerja]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

# ------------------------ OUTPUT ------------------------
if res.success:
    x_opt, y_opt = res.x
    z_opt = -res.fun

    st.success("✅ Solusi optimal ditemukan!")
    st.write(f"**Banner (x)**: `{x_opt:.2f}` unit")
    st.write(f"**Brosur (y)**: `{y_opt:.2f}` unit")
    st.write(f"**Keuntungan Maksimum**: `Rp {z_opt:,.0f}`")
    st.write(f"**Total Kapasitas Tenaga Kerja**: `{total_tenaga_kerja} jam` dari `{jumlah_karyawan}` orang")

    # Area Feasible
    st.subheader("📐 Grafik Area Feasible")
    x_vals = np.linspace(0, 100, 400)
    y_mesin = (kap_mesin - m_x * x_vals) / m_y
    y_bahan = (kap_bahan - b_x * x_vals) / b_y
    y_tenaga = (total_tenaga_kerja - t_x * x_vals) / t_y
    y_feasible = np.minimum(np.minimum(y_mesin, y_bahan), y_tenaga)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_mesin, label="Mesin")
    ax.plot(x_vals, y_bahan, label="Bahan Baku")
    ax.plot(x_vals, y_tenaga, label="Tenaga Kerja")
    ax.fill_between(x_vals, 0, y_feasible, where=(y_feasible >= 0), alpha=0.3, color='gray', label="Feasible Area")
    ax.plot(x_opt, y_opt, 'ro', label="Solusi Optimal")

    ax.set_xlabel("Banner (x)")
    ax.set_ylabel("Brosur (y)")
    ax.set_xlim(0, max(x_vals))
    ax.set_ylim(0, max(y_feasible[~np.isnan(y_feasible)]) + 10)
    ax.legend()
    st.pyplot(fig)

    # Grafik Keuangan
    st.subheader("💰 Grafik Keuangan Mingguan")
    pendapatan = x_opt * profit_x + y_opt * profit_y
    biaya_var = x_opt * cost_x + y_opt * cost_y
    total_biaya = biaya_var + fixed_cost
    laba = pendapatan - total_biaya

    fig2, ax2 = plt.subplots()
    labels = ['Pendapatan', 'Biaya Variabel', 'Biaya Tetap', 'Laba Bersih']
    values = [pendapatan, biaya_var, fixed_cost, laba]
    colors = ['green', 'orange', 'red', 'blue']
    bars = ax2.bar(labels, values, color=colors)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 50000, f"Rp {h:,.0f}", ha='center')
    ax2.set_ylabel("Rupiah (Rp)")
    ax2.set_title("Keuangan Mingguan")
    st.pyplot(fig2)

else:
    st.error("❌ Gagal menemukan solusi optimal.")
