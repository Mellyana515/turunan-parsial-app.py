import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Judul aplikasi
st.title("📈 Aplikasi Analisis Laba Industri - PT Makmur Jaya")

# Tab navigasi
with st.sidebar:
    tab = st.radio("Pilih Analisis:", ["Optimasi Produksi", "Model Persediaan (EOQ)", "Model Antrian (M/M/1)", "Turunan Parsial"])

# 1️⃣ Optimasi Produksi
if tab == "Optimasi Produksi":
    st.header("🔧 Optimasi Produksi - Linear Programming")
    st.markdown("### Studi Kasus PT Makmur Jaya")

    st.markdown("""
    Produk A memberikan laba Rp10.000 dan membutuhkan 2 jam kerja & 4 bahan baku.
    Produk B memberikan laba Rp8.000 dan membutuhkan 4 jam kerja & 2 bahan baku.
    Batasan: Maksimal 100 jam kerja dan 80 unit bahan baku.
    """)

    # Fungsi objektif: Maksimalkan 10.000x + 8.000y (ubah jadi minimisasi - karena linprog)
    c = [-10000, -8000]
    A = [[2, 4], [4, 2]]
    b = [100, 80]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    if res.success:
        st.success("Solusi optimal ditemukan!")
        st.write(f"Jumlah Produk A: {res.x[0]:.2f}")
        st.write(f"Jumlah Produk B: {res.x[1]:.2f}")
        st.write(f"Laba Maksimum: Rp{-res.fun:,.0f}")
    else:
        st.error("Gagal menemukan solusi optimal.")

# 2️⃣ Model Persediaan (EOQ)
elif tab == "Model Persediaan (EOQ)":
    st.header("📦 Model Persediaan - EOQ")
    st.markdown("""
    Permintaan tahunan bahan baku: 10.000 unit  
    Biaya pemesanan: Rp100.000 per kali pesan  
    Biaya penyimpanan: Rp2.000 per unit per tahun
    """)

    D = st.number_input("Permintaan tahunan (D):", value=10000)
    S = st.number_input("Biaya pemesanan per order (S):", value=100000)
    H = st.number_input("Biaya penyimpanan per unit per tahun (H):", value=2000)

    try:
        EOQ = ((2 * D * S) / H) ** 0.5
        st.success(f"Jumlah optimal pemesanan (EOQ): {EOQ:.2f} unit")
    except:
        st.error("Input tidak valid")

# 3️⃣ Model Antrian (M/M/1)
elif tab == "Model Antrian (M/M/1)":
    st.header("👥 Model Antrian - M/M/1")
    st.markdown("""
    Rata-rata kedatangan (λ): 8 pekerja per jam  
    Rata-rata pelayanan (μ): 10 pekerja per jam
    """)

    lam = st.number_input("Tingkat kedatangan rata-rata (λ):", value=8.0)
    mu = st.number_input("Tingkat pelayanan rata-rata (μ):", value=10.0)

    if lam >= mu:
        st.error("Sistem tidak stabil (λ ≥ μ), antrean akan terus bertambah!")
    else:
        rho = lam / mu
        Lq = rho**2 / (1 - rho)
        Wq = Lq / lam
        L = rho / (1 - rho)
        W = L / lam

        st.success("Hasil Analisis:")
        st.write(f"Rasio utilisasi server (ρ): {rho:.2f}")
        st.write(f"Rata-rata panjang antrean (Lq): {Lq:.2f} orang")
        st.write(f"Rata-rata waktu tunggu (Wq): {Wq:.2f} jam")
        st.write(f"Rata-rata jumlah orang dalam sistem (L): {L:.2f}")
        st.write(f"Rata-rata waktu dalam sistem (W): {W:.2f} jam")

# 4️⃣ Turunan Parsial
elif tab == "Turunan Parsial":
    st.header("📉 Analisis Turunan Parsial Fungsi Laba")
    st.markdown(r"""
    Fungsi laba:  
    \( f(x, y) = 10x + 8y - 0.1x^2 - 0.05y^2 \)
""")

    x, y = sp.symbols('x y')
    fungsi_str = st.text_input("Masukkan fungsi f(x, y):", "10*x + 8*y - 0.1*x**2 - 0.05*y**2")

    try:
        f = sp.sympify(fungsi_str)
        fx = sp.diff(f, x)
        fy = sp.diff(f, y)

        st.latex(f"f(x, y) = {sp.latex(f)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
        st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")

        x0 = st.number_input("Nilai x₀ (Produk A):", value=10.0)
        y0 = st.number_input("Nilai y₀ (Produk B):", value=10.0)

        f_val = f.subs({x: x0, y: y0})
        fx_val = fx.subs({x: x0, y: y0})
        fy_val = fy.subs({x: x0, y: y0})

        st.write(f"Nilai fungsi di titik (x₀, y₀): {f_val}")
        st.write(f"Gradien di titik (x₀, y₀): ({fx_val}, {fy_val})")

        st.subheader("Grafik Permukaan & Bidang Singgung")

        x_vals = np.linspace(x0 - 2, x0 + 2, 50)
        y_vals = np.linspace(y0 - 2, y0 + 2, 50)
        X, Y = np.meshgrid(x_vals, y_vals)

        f_lambdified = sp.lambdify((x, y), f, 'numpy')
        Z = f_lambdified(X, Y)

        Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')
        ax.plot_surface(X, Y, Z_tangent, alpha=0.5, color='red')
        ax.set_title("Permukaan f(x, y) dan bidang singgungnya")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
