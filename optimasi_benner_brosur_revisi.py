import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.optimize import linprog

# Konfigurasi halaman
st.set_page_config(page_title="Optimasi Produksi Banner & Brosur", layout="centered")
st.title("📈 Optimasi Produksi Banner dan Brosur")

st.markdown("""
Aplikasi ini menyelesaikan masalah Linear Programming (LP) untuk menentukan jumlah produksi optimal **banner** dan **brosur** agar **keuntungan maksimal** tercapai berdasarkan keterbatasan sumber daya.
""")

# Parameter produksi dan keuntungan
profit_x = 90000  # Banner
profit_y = 20000  # Brosur

# Kapasitas sumber daya
max_mesin = 150
max_bahan = 200
max_tenaga = 200

# Matriks kendala
A = [
    [1.0, 0.5],   # Mesin
    [2.0, 2.0],   # Bahan baku
    [2.0, 1.0]    # Tenaga kerja
]
b = [max_mesin, max_bahan, max_tenaga]

# Fungsi objektif (negatif untuk maksimasi)
c = [-profit_x, -profit_y]

# Batas variabel
x_bounds = (0, None)
y_bounds = (0, None)

# Optimasi Linear Programming
res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method="highs")

if res.success:
    x_opt = res.x[0]
    y_opt = res.x[1]
    z_opt = -res.fun

    st.success("✅ Solusi Optimal Ditemukan!")
    st.write(f"**Jumlah Banner (x):** {x_opt:.2f} unit")
    st.write(f"**Jumlah Brosur (y):** {y_opt:.2f} unit")
    st.write(f"**Total Keuntungan Maksimum:** Rp {z_opt:,.0f}")

    # Visualisasi Feasible Region (matplotlib)
    st.subheader("📊 Grafik Daerah Feasible & Titik Optimum")
    fig, ax = plt.subplots()

    x_vals = np.linspace(0, 100, 400)
    y1 = (max_mesin - 1.0 * x_vals) / 0.5  # Mesin
    y2 = (max_bahan - 2.0 * x_vals) / 2.0  # Bahan
    y3 = (max_tenaga - 2.0 * x_vals) / 1.0  # Tenaga kerja

    ax.plot(x_vals, y1, label="Mesin")
    ax.plot(x_vals, y2, label="Bahan Baku")
    ax.plot(x_vals, y3, label="Tenaga Kerja")

    y_max = np.minimum(np.minimum(y1, y2), y3)
    y_max = np.where(y_max < 0, 0, y_max)
    ax.fill_between(x_vals, 0, y_max, alpha=0.3)

    ax.plot(x_opt, y_opt, "ro", label="Solusi Optimal")
    ax.set_xlim(0, max(x_opt, 100))
    ax.set_ylim(0, max(y_opt, 120))
    ax.set_xlabel("Banner (x)")
    ax.set_ylabel("Brosur (y)")
    ax.set_title("Daerah Feasible dan Titik Optimal")
    ax.legend()
    st.pyplot(fig)

    # Visualisasi Produksi Optimal (Plotly)
    st.subheader("📦 Diagram Produksi Optimal (Interaktif)")
    df_prod = pd.DataFrame({
        "Produk": ["Banner", "Brosur"],
        "Jumlah Produksi": [x_opt, y_opt]
    })

    fig_bar = px.bar(
        df_prod,
        x="Produk",
        y="Jumlah Produksi",
        color="Produk",
        text="Jumlah Produksi",
        title="Diagram Produksi Optimal",
        labels={"Jumlah Produksi": "Unit"},
        color_discrete_sequence=["#636EFA", "#EF553B"]
    )

    fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pemanfaatan sumber daya
    st.subheader("🧰 Pemanfaatan Sumber Daya")
    waktu_mesin = 1.0 * x_opt + 0.5 * y_opt
    bahan_baku = 2.0 * x_opt + 2.0 * y_opt
    tenaga_kerja = 2.0 * x_opt + 1.0 * y_opt

    st.write(f"- Total Waktu Mesin: {waktu_mesin:.2f} jam / {max_mesin} jam")
    st.write(f"- Total Bahan Baku: {bahan_baku:.2f} unit / {max_bahan} unit")
    st.write(f"- Total Tenaga Kerja: {tenaga_kerja:.2f} jam / {max_tenaga} jam")

    # Estimasi jumlah tenaga kerja
    st.subheader("👷 Estimasi Jumlah Tenaga Kerja")
    jam_kerja_per_orang = 110
    kebutuhan_orang = np.ceil(tenaga_kerja / jam_kerja_per_orang)
    st.write(f"🧑‍🔧 Total jam kerja: {tenaga_kerja:.2f} jam → Dibutuhkan minimal **{int(kebutuhan_orang)} orang tenaga kerja**")

else:
    st.error("❌ Optimasi gagal. Silakan cek kembali parameter atau batasan kendala.")
