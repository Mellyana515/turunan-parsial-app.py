import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Aplikasi Studi Kasus Industri")

menu = st.radio("📌 Pilih Studi Kasus:", 
                ["Produksi Ban (Optimasi)", 
                 "Pengadaan Karet (EOQ)", 
                 "Antrian Bengkel", 
                 "Analisis Harga (Turunan Parsial)"])

if menu == "Pengadaan Karet (EOQ)":
    st.header("Pengadaan Karet - EOQ")

    # Input
    D = st.number_input("Permintaan Tahunan (unit)", value=10000)
    S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
    H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

    # Perhitungan EOQ
    EOQ = int(np.sqrt((2 * D * S) / H))

    st.subheader("Hasil Perhitungan:")
    st.write(f"🔹 EOQ (Jumlah Ekonomis Pemesanan) = **{EOQ} unit**")

    # Grafik Batang Permintaan vs EOQ
    fig, ax = plt.subplots()
    ax.bar(["Permintaan", "EOQ"], [D, EOQ], color=["red", "green"])
    ax.set_title("EOQ dan Permintaan Tahunan")
    ax.set_ylabel("Jumlah Unit")
    st.pyplot(fig)
