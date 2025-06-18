import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog  # type: ignore

st.set_page_config(page_title="Aplikasi Studi Kasus Industri", layout="wide")
st.title("📊 Aplikasi Analisis Model Matematika untuk Industri Ban")

with st.sidebar:
    tab = st.radio("📌 Pilih Studi Kasus:", [
        "Produksi Ban (Optimasi)", 
        "Pengadaan Karet (EOQ)", 
        "Antrian Bengkel", 
        "Analisis Harga (Turunan Parsial)"
    ])

# 1️⃣ Optimasi Produksi
if tab == "Produksi Ban (Optimasi)":
    st.header("🚗 Produksi Ban Mobil & Truk - Optimasi Laba")

    st.latex("Z = 50000x + 80000y")
    st.latex("2x + 4y \\leq 1200 \\quad \\text{(Jam Mesin)}")
    st.latex("4x + 5y \\leq 1600 \\quad \\text{(Bahan Karet)}")
    st.latex("x, y \\geq 0")

    c = [-50000, -80000]
    A = [[2, 4], [4, 5]]
    b = [1200, 1600]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))
    if res.success:
        x_opt, y_opt = res.x
        st.success(f"Produksi optimal: Ban Mobil = {x_opt:.2f}, Ban Truk = {y_opt:.2f}")
        st.write(f"Laba Maksimum: Rp {-res.fun:,.0f}")

        x_vals = np.linspace(0, 300, 200)
        y1 = (1200 - 2 * x_vals) / 4
        y2 = (1600 - 4 * x_vals) / 5

        fig, ax = plt.subplots()
        ax.plot(x_vals, y1, label="2x + 4y ≤ 1200")
        ax.plot(x_vals, y2, label="4x + 5y ≤ 1600")
        ax.fill_between(x_vals, np.minimum(y1, y2), 0, alpha=0.3)
        ax.plot(x_opt, y_opt, 'ro', label='Solusi Optimal')
        ax.set_xlabel("Ban Mobil (x)")
        ax.set_ylabel("Ban Truk (y)")
        ax.legend()
        st.pyplot(fig)

# 2️⃣ EOQ
elif tab == "Pengadaan Karet (EOQ)":
    st.header("📦 Pengadaan Karet Mentah - EOQ")

    st.markdown("""
    Economic Order Quantity (EOQ) adalah metode untuk menentukan jumlah pemesanan bahan baku agar total biaya tahunan minimum.
    
    ### Rumus:
    EOQ = √(2DS / H)
    """)

    D = st.number_input("Permintaan Tahunan (kg)", value=50000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=250000)
    H = st.number_input("Biaya Penyimpanan per Tahun (Rp/kg)", value=1000)

    EOQ = ((2 * D * S) / H) ** 0.5
    OC = (D / EOQ) * S
    HC = (EOQ / 2) * H
    TC = OC + HC

    st.subheader("📈 Hasil Perhitungan:")
    st.write(f"EOQ optimal: **{EOQ:.2f} kg**")
    st.write(f"- Biaya Pemesanan: Rp {OC:,.0f}")
    st.write(f"- Biaya Penyimpanan: Rp {HC:,.0f}")
    st.write(f"- Total Biaya Tahunan: **Rp {TC:,.0f}**")

    # Grafik dalam bentuk persentase agar tidak datar
    Q = np.linspace(EOQ * 0.4, EOQ * 1.6, 300)
    OC_curve = (D / Q) * S
    HC_curve = (Q / 2) * H
    TC_curve = OC_curve + HC_curve

    TC_min = TC_curve.min()
    OC_curve_pct = (OC_curve / TC_min) * 100
    HC_curve_pct = (HC_curve / TC_min) * 100
    TC_curve_pct = (TC_curve / TC_min) * 100

    fig, ax = plt.subplots()
    ax.plot(Q, TC_curve_pct, label="Total Cost (%)", color='blue', linewidth=2)
    ax.plot(Q, OC_curve_pct, label="Ordering Cost (%)", color='green', linestyle='--')
    ax.plot(Q, HC_curve_pct, label="Holding Cost (%)", color='orange', linestyle='--')
    ax.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.0f}')
    ax.scatter([EOQ], [100], color='red')
    ax.annotate(f"EOQ = {EOQ:.0f} kg\n100% Biaya Minimum",
                (EOQ, 100),
                xytext=(10, -30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color='gray'))
    ax.set_xlabel("Jumlah Pembelian (Q)")
    ax.set_ylabel("Biaya (% dari minimum)")
    ax.set_title("Kurva EOQ (Dalam Persentase agar Tampak Jelas)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    st.pyplot(fig)

# 3️⃣ Antrian Bengkel
elif tab == "Antrian Bengkel":
    st.header("⏱️ Antrian Pelanggan di Bengkel Ban - M/M/1")

    st.latex("\\rho = \\frac{\\lambda}{\\mu}")
    st.latex("L = \\frac{\\rho}{1 - \\rho}, \\quad L_q = \\frac{\\rho^2}{1 - \\rho}")
    st.latex("W = \\frac{1}{\\mu - \\lambda}, \\quad W_q = \\frac{\\rho}{\\mu - \\lambda}")

    lam = st.number_input("Tingkat Kedatangan λ (pelanggan/jam)", value=6.0)
    mu = st.number_input("Tingkat Pelayanan μ (pelanggan/jam)", value=10.0)

    if lam >= mu:
        st.error("Sistem tidak stabil (λ ≥ μ)")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = L / lam
        Wq = Lq / lam

        st.success("Sistem Stabil")
        st.write(f"Utilisasi (ρ): {rho:.2f}")
        st.write(f"Rata-rata pelanggan di sistem (L): {L:.2f}")
        st.write(f"Rata-rata waktu dalam sistem (W): {W:.2f} jam")
        st.write(f"Rata-rata antrean (Lq): {Lq:.2f}")
        st.write(f"Waktu tunggu dalam antrean (Wq): {Wq:.2f} jam")

        fig, ax = plt.subplots()
        ax.bar(["L", "Lq", "W", "Wq"], [L, Lq, W, Wq], color=['blue', 'orange', 'green', 'red'])
        ax.set_title("Grafik Kinerja Antrian Bengkel")
        st.pyplot(fig)

# 4️⃣ Turunan Parsial
elif tab == "Analisis Harga (Turunan Parsial)":
    st.header("📈 Analisis Harga Ban terhadap Laba - Turunan Parsial")

    x, y = sp.symbols("x y")
    st.latex("f(x, y) = 10000x + 15000y - 0.1x^2 - 0.05y^2")

    f = 10000 * x + 15000 * y - 0.1 * x**2 - 0.05 * y**2
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {sp.latex(fx)}")
    st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {sp.latex(fy)}")

    x0 = st.number_input("Harga Ban Mobil (x)", value=20.0)
    y0 = st.number_input("Harga Ban Truk (y)", value=30.0)

    f_val = f.subs({x: x0, y: y0})
    fx_val = fx.subs({x: x0, y: y0})
    fy_val = fy.subs({x: x0, y: y0})

    st.write(f"Laba f({x0}, {y0}) = Rp {float(f_val):,.0f}")
    st.write(f"∂f/∂x = Rp {float(fx_val):,.0f}  |  ∂f/∂y = Rp {float(fy_val):,.0f}")

    X_vals = np.linspace(x0 - 5, x0 + 5, 50)
    Y_vals = np.linspace(y0 - 5, y0 + 5, 50)
    X, Y = np.meshgrid(X_vals, Y_vals)
    f_np = sp.lambdify((x, y), f, "numpy")
    Z = f_np(X, Y)
    Z_tangent = float(f_val) + float(fx_val) * (X - x0) + float(fy_val) * (Y - y0)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.7)
    ax.plot_surface(X, Y, Z_tangent, color="red", alpha=0.4)
    ax.set_title("Permukaan Laba dan Bidang Singgung")
    ax.set_xlabel("Harga Ban Mobil (x)")
    ax.set_ylabel("Harga Ban Truk (y)")
    ax.set_zlabel("Laba")
    st.pyplot(fig)
