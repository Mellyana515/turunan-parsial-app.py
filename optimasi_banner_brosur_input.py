
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Judul Aplikasi
st.title("📈 Optimasi Produksi Banner dan Brosur")

st.write("""
Masukkan parameter produksi dan batasan sumber daya untuk menentukan jumlah produksi optimal.
""")

# Input manual dari pengguna
profit_x = st.number_input("Keuntungan per unit Banner (Rp)", min_value=1000, value=90000, step=1000)
profit_y = st.number_input("Keuntungan per unit Brosur (Rp)", min_value=1000, value=20000, step=1000)

machine_hours = st.number_input("Kapasitas Waktu Mesin (jam/bulan)", min_value=1, value=150)
material_units = st.number_input("Kapasitas Bahan Baku (unit/bulan)", min_value=1, value=200)
labor_hours = st.number_input("Kapasitas Tenaga Kerja (jam/bulan)", min_value=1, value=200)

# Koefisien kebutuhan per unit
st.markdown("### ⏱️ Waktu Mesin per Unit")
machine_x = st.number_input("Banner (jam)", min_value=0.0, value=1.0)
machine_y = st.number_input("Brosur (jam)", min_value=0.0, value=0.5)

st.markdown("### 🧱 Bahan Baku per Unit")
material_x = st.number_input("Banner (unit)", min_value=0.0, value=2.0)
material_y = st.number_input("Brosur (unit)", min_value=0.0, value=2.0)

st.markdown("### 🧑‍🏭 Tenaga Kerja per Unit")
labor_x = st.number_input("Banner (jam)", min_value=0.0, value=2.0)
labor_y = st.number_input("Brosur (jam)", min_value=0.0, value=1.0)

# Koefisien kendala
A = [
    [machine_x, machine_y],
    [material_x, material_y],
    [labor_x, labor_y]
]
b = [machine_hours, material_units, labor_hours]
c = [-profit_x, -profit_y]
x_bounds = (0, None)
y_bounds = (0, None)

# Tombol jalankan optimasi
if st.button("🔍 Jalankan Optimasi"):
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

    if res.success:
        x = res.x[0]
        y = res.x[1]
        total_profit = -(res.fun)

        st.success("✅ Solusi Optimal Ditemukan:")
        st.write(f"Jumlah **Banner (x)** yang diproduksi: `{x:.2f}` unit")
        st.write(f"Jumlah **Brosur (y)** yang diproduksi: `{y:.2f}` unit")
        st.write(f"Total Keuntungan Maksimal: `Rp {total_profit:,.0f}`")

        # Visualisasi grafik area feasible
        st.subheader("📊 Grafik Daerah Feasible & Solusi Optimal")

        x_vals = np.linspace(0, 200, 400)
        y1 = (machine_hours - machine_x * x_vals) / machine_y
        y2 = (material_units - material_x * x_vals) / material_y
        y3 = (labor_hours - labor_x * x_vals) / labor_y

        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y1, label='Kendala Waktu Mesin')
        plt.plot(x_vals, y2, label='Kendala Bahan Baku')
        plt.plot(x_vals, y3, label='Kendala Tenaga Kerja')
        plt.fill_between(x_vals, np.minimum(np.minimum(y1, y2), y3), color='skyblue', alpha=0.4)
        plt.plot(x, y, 'ro', label='Solusi Optimal')
        plt.xlim(0, max(x_vals))
        plt.ylim(0, max(max(y1), max(y2), max(y3)))
        plt.xlabel("Banner (x)")
        plt.ylabel("Brosur (y)")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Visualisasi batang jumlah produksi
        st.subheader("📦 Diagram Produksi")
        fig2, ax2 = plt.subplots()
        ax2.bar(["Banner", "Brosur"], [x, y], color=["blue", "green"])
        ax2.set_ylabel("Unit Produksi")
        st.pyplot(fig2)

    else:
        st.error("❌ Tidak ditemukan solusi optimal.")
