
import streamlit as st
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Aplikasi Optimasi Produksi Banner dan Brosur")

st.markdown("""
Aplikasi ini membantu menentukan jumlah optimal produksi banner dan brosur untuk memaksimalkan keuntungan berdasarkan batasan sumber daya.
""")

# Parameter keuntungan
profit_banner = 90000
profit_brosur = 20000

# Input batasan
st.sidebar.header("Input Batasan Sumber Daya per Bulan")
mesin = st.sidebar.number_input("Kapasitas Mesin (jam)", value=150)
bahan = st.sidebar.number_input("Kapasitas Bahan Baku (unit)", value=200)
tenaga = st.sidebar.number_input("Kapasitas Tenaga Kerja (jam)", value=200)

# Matriks koefisien kendala
A = [
    [1, 0.5],  # waktu mesin
    [2, 2],    # bahan baku
    [2, 1]     # tenaga kerja
]

b = [mesin, bahan, tenaga]

# Fungsi tujuan (koefisien negatif karena linprog melakukan minimisasi)
c = [-profit_banner, -profit_brosur]

# Batasan variabel (x ≥ 0, y ≥ 0)
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    x_opt = res.x[0]
    y_opt = res.x[1]
    total_profit = -(res.fun)

    st.subheader("🔎 Hasil Optimasi")
    st.write(f"Jumlah optimal produksi **Banner** (x): `{x_opt:.2f}` unit")
    st.write(f"Jumlah optimal produksi **Brosur** (y): `{y_opt:.2f}` unit")
    st.write(f"Keuntungan maksimum: `Rp {total_profit:,.0f}`")

    # Visualisasi Bar
    st.subheader("📊 Visualisasi Produksi Optimal")
    fig, ax = plt.subplots()
    ax.bar(["Banner", "Brosur"], [x_opt, y_opt], color=['blue', 'green'])
    ax.set_ylabel("Jumlah Produksi (unit)")
    st.pyplot(fig)

    # Visualisasi Pemanfaatan Sumber Daya
    st.subheader("📈 Pemanfaatan Sumber Daya")
    waktu_dipakai = [x_opt * 1 + y_opt * 0.5,
                     x_opt * 2 + y_opt * 2,
                     x_opt * 2 + y_opt * 1]

    sumber_daya = ["Waktu Mesin", "Bahan Baku", "Tenaga Kerja"]
    fig2, ax2 = plt.subplots()
    ax2.barh(sumber_daya, waktu_dipakai, color='orange', label="Terpakai")
    ax2.barh(sumber_daya, [mesin, bahan, tenaga], color='grey', alpha=0.3, label="Kapasitas")
    ax2.legend()
    st.pyplot(fig2)

else:
    st.error("Optimasi gagal dilakukan. Silakan cek kembali input parameter.")
