
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Judul Aplikasi
st.title("📈 Optimasi Produksi Banner dan Brosur")

st.write("""
Aplikasi ini menggunakan Linear Programming untuk menentukan jumlah produksi optimal dari dua produk:
**Banner (x)** dan **Brosur (y)**, berdasarkan kendala waktu mesin, bahan baku, dan tenaga kerja.
""")

# Parameter keuntungan
profit_x = 90000
profit_y = 20000

# Kendala sumber daya
machine_hours = 150
material_units = 200
labor_hours = 200

# Koefisien kendala (diambil dari laporan)
A = [
    [1.0, 0.5],    # waktu mesin
    [2.0, 2.0],    # bahan baku
    [2.0, 1.0]     # tenaga kerja
]

b = [machine_hours, material_units, labor_hours]

# Fungsi objektif (dikalikan -1 karena linprog meminimasi)
c = [-profit_x, -profit_y]

# Batasan x dan y harus >= 0
x_bounds = (0, None)
y_bounds = (0, None)

# Optimisasi Linear Programming
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

    x_vals = np.linspace(0, 150, 400)
    y1 = (machine_hours - A[0][0]*x_vals) / A[0][1]
    y2 = (material_units - A[1][0]*x_vals) / A[1][1]
    y3 = (labor_hours - A[2][0]*x_vals) / A[2][1]

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
