
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Judul aplikasi
st.title("📈 Optimasi Produksi Benner dan Brosur")

st.write("""
Aplikasi ini menggunakan Linear Programming untuk menentukan jumlah produksi optimal dari dua produk:
**Benner** dan **Brosur**, dengan mempertimbangkan batasan sumber daya, biaya tetap, dan simulasi multi-minggu.
""")

# Sidebar Input
st.sidebar.header("Input Parameter Produksi")

# Keuntungan per unit
profit_x = st.sidebar.number_input("Keuntungan per unit Benner (Rp)", value=60000)
profit_y = st.sidebar.number_input("Keuntungan per unit Brosur (Rp)", value=5000)

st.sidebar.subheader("Konsumsi Sumber Daya per Unit")
machine_x = st.sidebar.number_input("Waktu Mesin per Benner (jam)", value=3.0)
machine_y = st.sidebar.number_input("Waktu Mesin per Brosur (jam)", value=0.1)
material_x = st.sidebar.number_input("Bahan Baku per Benner (unit)", value=2.0)
material_y = st.sidebar.number_input("Bahan Baku per Brosur (unit)", value=3.0)
labor_x = st.sidebar.number_input("Tenaga Kerja per Benner (jam)", value=2.0)
labor_y = st.sidebar.number_input("Tenaga Kerja per Brosur (jam)", value=0.2)

st.sidebar.subheader("Batasan Total Sumber Daya")
machine_limit = st.sidebar.number_input("Total Waktu Mesin (jam)", value=120.0)
material_limit = st.sidebar.number_input("Total Bahan Baku (unit)", value=150.0)
labor_limit = st.sidebar.number_input("Total Tenaga Kerja (jam)", value=160.0)

st.sidebar.subheader("Simulasi Mingguan")
weeks = st.sidebar.slider("Jumlah Minggu Simulasi", min_value=1, max_value=12, value=4)
fixed_cost_per_week = st.sidebar.number_input("Biaya Tetap Mingguan (Rp)", value=1500000)

# Fungsi Objektif
c = [-profit_x, -profit_y]
A = [
    [machine_x, machine_y],
    [material_x, material_y],
    [labor_x, labor_y]
]
b = [machine_limit, material_limit, labor_limit]
bounds = [(0, None), (0, None)]

# Optimasi
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

if res.success:
    x_opt, y_opt = res.x
    total_profit_week = -res.fun
    used_machine = machine_x * x_opt + machine_y * y_opt

    st.subheader("📊 Hasil Optimasi")
    st.write(f"Jumlah Benner (x): **{x_opt:.2f} unit**")
    st.write(f"Jumlah Brosur (y): **{y_opt:.2f} unit**")
    st.write(f"Keuntungan Kotor / Minggu: **Rp {total_profit_week:,.0f}**")

    st.write("### 📈 Pemanfaatan Sumber Daya")
    st.write(f"- Waktu Mesin: {used_machine:.1f} jam / {machine_limit} jam ({used_machine/machine_limit*100:.1f}%)")

    # Estimasi Hari Kerja
    st.write("### 🕒 Estimasi Hari Kerja")
    hari_1_shift = used_machine / 8
    hari_2_shift = used_machine / 16
    st.write(f"- 1 Shift (8 jam/hari): {hari_1_shift:.1f} → dibulatkan: {np.ceil(hari_1_shift)} hari")
    st.write(f"- 2 Shift (16 jam/hari): {hari_2_shift:.1f} → dibulatkan: {np.ceil(hari_2_shift)} hari")

    # Simulasi Multi-Minggu
    st.subheader("📅 Simulasi Multi-Minggu")
    total_gross = total_profit_week * weeks
    total_fixed_cost = fixed_cost_per_week * weeks
    net_profit = total_gross - total_fixed_cost

    st.write(f"- Total Keuntungan Kotor ({weeks} minggu): Rp {total_gross:,.0f}")
    st.write(f"- Total Biaya Tetap ({weeks} minggu): Rp {total_fixed_cost:,.0f}")
    st.write(f"💰 **Keuntungan Bersih Total: Rp {net_profit:,.0f}**")

else:
    st.error("❌ Optimasi gagal. Periksa kembali input parameter.")
