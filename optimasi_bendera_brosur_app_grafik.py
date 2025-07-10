
import streamlit as st
import numpy as np
from scipy.optimize import linprog

st.title("📈 Optimasi Produksi Bendera dan Brosur")

st.write("""
Aplikasi ini menggunakan Linear Programming untuk memaksimalkan keuntungan dari produksi dua produk: **bendera** dan **brosur**,
dengan mempertimbangkan batasan waktu mesin, bahan baku, dan tenaga kerja.
""")

# Input user
st.sidebar.header("Input Parameter Produksi")
profit_x = st.sidebar.number_input("Keuntungan per unit Bendera (Rp)", value=60000)
profit_y = st.sidebar.number_input("Keuntungan per unit Brosur (Rp)", value=5000)

st.sidebar.subheader("Konsumsi Sumber Daya per Unit")
machine_x = st.sidebar.number_input("Waktu Mesin per Bendera (jam)", value=3.0)
machine_y = st.sidebar.number_input("Waktu Mesin per Brosur (jam)", value=0.1)
material_x = st.sidebar.number_input("Bahan per Bendera (unit)", value=2.0)
material_y = st.sidebar.number_input("Bahan per Brosur (unit)", value=3.0)
labor_x = st.sidebar.number_input("Tenaga Kerja per Bendera (jam)", value=2.0)
labor_y = st.sidebar.number_input("Tenaga Kerja per Brosur (jam)", value=0.2)

st.sidebar.subheader("Batasan Total Sumber Daya")
machine_limit = st.sidebar.number_input("Total Waktu Mesin (jam)", value=120.0)
material_limit = st.sidebar.number_input("Total Bahan (unit)", value=150.0)
labor_limit = st.sidebar.number_input("Total Tenaga Kerja (jam)", value=160.0)

# Fungsi objektif (negatif karena linprog meminimalkan)
c = [-profit_x, -profit_y]

# Kendala matriks
A = [
    [machine_x, machine_y],
    [material_x, material_y],
    [labor_x, labor_y]
]
b = [machine_limit, material_limit, labor_limit]

# Batasan x ≥ 0 dan y ≥ 0
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method="highs")

if res.success:
    x_opt, y_opt = res.x
    total_profit = -(res.fun)

    st.subheader("🔍 Hasil Optimasi")
    st.write(f"Jumlah Bendera (x): **{x_opt:.0f} unit**")
    st.write(f"Jumlah Brosur (y): **{y_opt:.0f} unit**")
    st.write(f"Total Keuntungan Maksimum: **Rp {total_profit:,.0f}**")

    import matplotlib.pyplot as plt

    # Tambah grafik visualisasi kendala dan solusi
    st.subheader("📉 Visualisasi Feasible Region dan Titik Optimal")

    # Buat rentang nilai x dan y
    x_vals = np.linspace(0, 80, 200)
    y1 = (machine_limit - machine_x * x_vals) / machine_y
    y2 = (material_limit - material_x * x_vals) / material_y
    y3 = (labor_limit - labor_x * x_vals) / labor_y

    # Gambar grafik
    fig, ax = plt.subplots()
    ax.plot(x_vals, y1, label="Waktu Mesin", color='blue')
    ax.plot(x_vals, y2, label="Bahan", color='green')
    ax.plot(x_vals, y3, label="Tenaga Kerja", color='red')
    ax.set_xlim((0, max(x_vals)))
    ax.set_ylim((0, max(np.nanmax(y1), np.nanmax(y2), np.nanmax(y3))))

    # Warnai area feasible
    y_all = np.minimum(np.minimum(y1, y2), y3)
    ax.fill_between(x_vals, 0, y_all, where=(y_all >= 0), color='gray', alpha=0.3)

    # Titik optimal
    ax.plot(x_opt, y_opt, 'ro', label='Titik Optimal')

    ax.set_xlabel("Jumlah Bendera (x)")
    ax.set_ylabel("Jumlah Brosur (y)")
    ax.set_title("Feasible Region & Titik Optimal")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


    # Pemanfaatan sumber daya
    used_machine = machine_x * x_opt + machine_y * y_opt
    used_material = material_x * x_opt + material_y * y_opt
    used_labor = labor_x * x_opt + labor_y * y_opt

    st.subheader("📊 Pemanfaatan Sumber Daya")
    st.write(f"Waktu Mesin: {used_machine:.1f} jam / {machine_limit} jam ({(used_machine/machine_limit)*100:.1f}%)")
    st.write(f"Bahan Baku: {used_material:.1f} unit / {material_limit} unit ({(used_material/material_limit)*100:.1f}%)")
    st.write(f"Tenaga Kerja: {used_labor:.1f} jam / {labor_limit} jam ({(used_labor/labor_limit)*100:.1f}%)")
else:
    st.error("Optimasi gagal. Silakan periksa input parameter.")
