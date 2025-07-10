mport streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="EOQ Brosur & Banner", layout="centered")

st.title("📦 EOQ Brosur & Banner - CV Kreatif Media")
st.markdown("Hitung jumlah pemesanan optimal untuk dua produk agar biaya persediaan minimum.")

# Input Data Brosur
st.subheader("📘 Input Data - Brosur")
D1 = st.number_input("Permintaan tahunan brosur (unit)", value=12000)
S1 = st.number_input("Biaya pemesanan per order (Rp)", value=150000)
H1 = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", value=500)

# Input Data Banner
st.subheader("📙 Input Data - Banner")
D2 = st.number_input("Permintaan tahunan banner (unit)", value=3000)
S2 = st.number_input("Biaya pemesanan per order (Rp)", value=180000)
H2 = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", value=2000)

# Hitung EOQ
EOQ1 = np.sqrt((2 * D1 * S1) / H1) if H1 > 0 else 0
EOQ2 = np.sqrt((2 * D2 * S2) / H2) if H2 > 0 else 0

# Total biaya persediaan
cost1 = (D1 / EOQ1) * S1 + (EOQ1 / 2) * H1 if EOQ1 > 0 else 0
cost2 = (D2 / EOQ2) * S2 + (EOQ2 / 2) * H2 if EOQ2 > 0 else 0
total = cost1 + cost2

# Output
st.markdown("## 🧮 Hasil Perhitungan EOQ")
st.write(f"**EOQ Brosur**: {EOQ1:.0f} unit/order")
st.write(f"**Total Biaya Persediaan Brosur**: Rp {cost1:,.0f}")

st.write(f"**EOQ Banner**: {EOQ2:.0f} unit/order")
st.write(f"**Total Biaya Persediaan Banner**: Rp {cost2:,.0f}")

st.success(f"📊 Total Biaya Persediaan Tahunan: Rp {total:,.0f}")

# --------------------
# 📈 Grafik Kurva EOQ
# --------------------
st.markdown("## 📉 Grafik Total Biaya vs Jumlah Pemesanan")

x_vals = np.arange(100, int(max(EOQ1, EOQ2)*2), 100)

def total_cost(D, S, H, Q):
    return (D / Q) * S + (Q / 2) * H

brosur_costs = total_cost(D1, S1, H1, x_vals)
banner_costs = total_cost(D2, S2, H2, x_vals)

fig, ax = plt.subplots()
ax.plot(x_vals, brosur_costs, label="Biaya Total Brosur", color="blue")
ax.axvline(EOQ1, color='blue', linestyle='--', label=f"EOQ Brosur: {EOQ1:.0f}")

ax.plot(x_vals, banner_costs, label="Biaya Total Banner", color="green")
ax.axvline(EOQ2, color='green', linestyle='--', label=f"EOQ Banner: {EOQ2:.0f}")

ax.set_xlabel("Jumlah Pemesanan per Order (unit)")
ax.set_ylabel("Total Biaya Persediaan (Rp)")
ax.set_title("Kurva EOQ - Biaya Total vs Jumlah Pemesanan")
ax.legend()
ax.grid(True)

st.pyplot(fig)
