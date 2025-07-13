import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(layout="centered")
st.title("🧮 Optimasi Produksi - Input Manual")

st.markdown("Masukkan parameter di bawah untuk mencari solusi optimal produksi 2 produk menggunakan Linear Programming.")

# ------------------------ INPUT ------------------------
st.sidebar.header("📥 Input Parameter")

# Keuntungan per unit
profit_x = st.sidebar.number_input("Keuntungan per unit Banner (Rp)", min_value=0, value=90000)
profit_y = st.sidebar.number_input("Keuntungan per unit Brosur (Rp)", min_value=0, value=20000)

# Biaya variabel
cost_x = st.sidebar.number_input("Biaya variabel per unit Banner", min_value=0, value=35000)
cost_y = st.sidebar.number_input("Biaya variabel per unit Brosur", min_value=0, value=10000)

# Biaya tetap mingguan
fixed_cost = st.sidebar.number_input("Biaya Tetap Mingguan (Rp)", min_value=0, value=675000)

# Kapasitas sumber daya
mesin = st.sidebar.number_input("Kapasitas Mesin (jam)", min_value=1, value=150)
bahan = st.sidebar.number_input("Kapasitas Bahan Baku (unit)", min_value=1, value=200)
tenaga = st.sidebar.number_input("Kapasitas Tenaga Kerja (jam)", min_value=1, value=200)

# Konsumsi per unit
m_x = st.sidebar.number_input("Jam Mesin / unit Banner", value=3.0)
m_y = st.sidebar.number_input("Jam Mesin / unit Brosur", value=0.5)

b_x = st.sidebar.number_input("Bahan Baku / unit Banner", value=2.0)
b_y = st.sidebar.number_input("Bahan Baku / unit Brosur", value=2.0)

t_x = st.sidebar.number_input("Jam Tenaga Kerja / unit Banner", value=2.0)
t_y = st.sidebar.number_input("Jam Tenaga Kerja / unit Brosur", value=1.0)

# ------------------------ LINEAR PROGRAMMING ------------------------
c = [-profit_x, -profit_y]  # Maksimasi → -min
A = [
    [m_x, m_y],
    [b_x, b_y],
    [t_x, t_y]
]
b = [mesin, bahan, tenaga]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

if res.success:
    x_opt, y_opt = res.x
    z_opt = -res.fun

    st.success("✅ Solusi optimal ditemukan!")
    st.markdown(f"- Produksi Banner: **{x_opt:.2f} unit**")
    st.markdown(f"- Produksi Brosur: **{y_opt:.2f} unit**")
    st.markdown(f"- Total Keuntungan Maksimum: **Rp {z_opt:,.0f}**")

    # Grafik Area Feasible
    st.subheader("📐 Visualisasi Area Feasible")
    x_vals = np.linspace(0, 100, 400)
    y_mesin = (mesin - m_x * x_vals) / m_y
    y_bahan = (bahan - b_x * x_vals) / b_y
    y_tenaga = (tenaga - t_x * x_vals) / t_y
    y_min = np.minimum(np.minimum(y_mesin, y_bahan), y_tenaga)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_mesin, label='Mesin')
    ax.plot(x_vals, y_bahan, label='Bahan Baku')
    ax.plot(x_vals, y_tenaga, label='Tenaga Kerja')
    ax.fill_between(x_vals, 0, y_min, where=(y_min >= 0), color='lightgray', alpha=0.5, label="Area Feasible")
    ax.plot(x_opt, y_opt, 'ro', label='Solusi Optimal')

    ax.set_xlim(0, max(x_vals))
    ax.set_ylim(0, max(y_min[~np.isnan(y_min)]) + 10)
    ax.set_xlabel("Banner (x)")
    ax.set_ylabel("Brosur (y)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Grafik Keuangan
    st.subheader("💰 Grafik Keuangan Mingguan")
    revenue = x_opt * profit_x + y_opt * profit_y
    biaya_var = x_opt * cost_x + y_opt * cost_y
    biaya_total = biaya_var + fixed_cost
    laba = revenue - biaya_total

    fig2, ax2 = plt.subplots()
    labels = ['Pendapatan', 'Biaya Variabel', 'Biaya Tetap', 'Laba Bersih']
    values = [revenue, biaya_var, fixed_cost, laba]
    colors = ['green', 'orange', 'red', 'blue']
    bars = ax2.bar(labels, values, color=colors)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 50000, f"Rp {h:,.0f}", ha='center')
    ax2.set_ylabel("Rupiah (Rp)")
    st.pyplot(fig2)

else:
    st.error("❌ Tidak ditemukan solusi optimal.")
