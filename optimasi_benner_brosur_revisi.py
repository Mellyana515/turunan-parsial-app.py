import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(layout="centered")
st.title("📦 Optimasi Produksi Banner dan Brosur")
st.markdown("Studi kasus linear programming untuk **memaksimalkan keuntungan** berdasarkan batasan sumber daya produksi.")

# ----------------------- DATA -----------------------
c = [-90000, -20000]  # Fungsi objektif (max → -min)

# Kendala produksi:
# 3x + 0.5y ≤ 150  (Mesin)
# 2x + 2y ≤ 200    (Bahan Baku)
# 2x + 1y ≤ 200    (Tenaga Kerja)
A = [
    [3, 0.5],
    [2, 2],
    [2, 1]
]
b = [150, 200, 200]

# Batasan variabel
bounds = [(0, None), (0, None)]

# ----------------------- OPTIMISASI -----------------------
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

if res.success:
    x_opt, y_opt = res.x
    max_profit = -res.fun

    st.success("✅ Solusi optimal ditemukan!")
    st.markdown(f"- Produksi Banner: **{x_opt:.2f} unit**")
    st.markdown(f"- Produksi Brosur: **{y_opt:.2f} unit**")
    st.markdown(f"- Total Keuntungan Maksimum: **Rp {max_profit:,.0f}**")

    # ----------------------- GRAFIK AREA FEASIBLE -----------------------
    st.subheader("📐 Visualisasi Area Feasible & Titik Optimal")
    x_vals = np.linspace(0, 80, 400)
    y1 = (150 - 3 * x_vals) / 0.5     # Mesin
    y2 = (200 - 2 * x_vals) / 2       # Bahan Baku
    y3 = (200 - 2 * x_vals)           # Tenaga Kerja

    fig1, ax1 = plt.subplots()
    ax1.plot(x_vals, y1, label='Mesin (3x + 0.5y ≤ 150)')
    ax1.plot(x_vals, y2, label='Bahan Baku (2x + 2y ≤ 200)')
    ax1.plot(x_vals, y3, label='Tenaga Kerja (2x + y ≤ 200)')

    ax1.fill_between(x_vals, 0, np.minimum(np.minimum(y1, y2), y3), where=(x_vals >= 0), color='lightgray', alpha=0.5, label='Area Feasible')
    ax1.plot(x_opt, y_opt, 'ro', label='Solusi Optimal')

    ax1.set_xlim(0, 80)
    ax1.set_ylim(0, 120)
    ax1.set_xlabel("Banner (x)")
    ax1.set_ylabel("Brosur (y)")
    ax1.set_title("Area Feasible dan Titik Solusi Optimal")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # ----------------------- GRAFIK JUMLAH PRODUKSI -----------------------
    st.subheader("📊 Grafik Produksi Optimal")
    fig2, ax2 = plt.subplots()
    produk = ['Banner', 'Brosur']
    jumlah = [x_opt, y_opt]
    bars = ax2.bar(produk, jumlah, color=['skyblue', 'lightgreen'])
    for i, val in enumerate(jumlah):
        ax2.text(i, val + 1, f"{val:.1f}", ha='center')
    ax2.set_ylabel("Jumlah Unit")
    ax2.set_title("Produksi Optimal")
    st.pyplot(fig2)

    # ----------------------- GRAFIK KEUANGAN -----------------------
    st.subheader("💰 Grafik Keuangan Mingguan")
    harga_banner, harga_brosur = 90000, 20000
    biaya_banner, biaya_brosur = 35000, 10000
    biaya_tetap = 2700000 / 4  # mingguan

    pendapatan = x_opt * harga_banner + y_opt * harga_brosur
    biaya_var = x_opt * biaya_banner + y_opt * biaya_brosur
    total_biaya = biaya_var + biaya_tetap
    laba_bersih = pendapatan - total_biaya

    labels = ['Pendapatan', 'Biaya Variabel', 'Biaya Tetap', 'Laba Bersih']
    values = [pendapatan, biaya_var, biaya_tetap, laba_bersih]
    colors = ['green', 'orange', 'red', 'blue']

    fig3, ax3 = plt.subplots()
    bar3 = ax3.bar(labels, values, color=colors)
    for bar in bar3:
        h = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, h + 10000, f"Rp {h:,.0f}", ha='center')
    ax3.set_ylabel("Rupiah (Rp)")
    ax3.set_title("Keuangan Produksi Mingguan")
    st.pyplot(fig3)

else:
    st.error("❌ Gagal menemukan solusi optimal.")
