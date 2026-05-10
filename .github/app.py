import streamlit as st
import matplotlib.pyplot as plt
import ternary

st.set_page_config(page_title="Pettijohn Classifier", layout="centered")

st.title("💎 Sandstone Classifier (Pettijohn, 1975)")
st.write("Projek Komputasi Geologist - Klasifikasi Sandstone berdasarkan QFL & Matriks.")

# Input Komposisi
col1, col2 = st.columns(2)
with col1:
    q = st.number_input("Quartz (%)", 0.0, 100.0, 40.0)
    f = st.number_input("Feldspar (%)", 0.0, 100.0, 10.0)
with col2:
    l = st.number_input("Lithic Fragments (%)", 0.0, 100.0, 50.0)
    m = st.number_input("Matrix (%)", 0.0, 100.0, 5.0)

total = q + f + l
if total > 0:
    # Normalisasi
    Q = (q / total) * 100
    F = (f / total) * 100
    L = (l / total) * 100

    # Logika Klasifikasi
    if m > 15:
        category = "Wacke"
        if Q > 95: name = "Quartz Wacke"
        elif F > L: name = "Feldspathic Wacke"
        else: name = "Lithic Wacke"
    else:
        category = "Arenite"
        if Q > 95: name = "Quartz Arenite"
        elif Q > 75: name = "Subarkose" if F > L else "Sublitharenite"
        else: name = "Arkose" if F > L else "Lithic Arenite"

    # Plotting
    fig, tax = ternary.figure(scale=100)
    tax.line((0, 95, 5), (5, 95, 0), linewidth=1, color='black')
    tax.line((0, 75, 25), (25, 75, 0), linewidth=1, color='black')
    tax.line((0, 100, 0), (50, 0, 50), linewidth=1, color='black')
    tax.scatter([(L, Q, F)], marker='o', color='yellow', s=150, edgecolors='black')
    tax.set_title(f"Hasil: {name}")
    tax.boundary(linewidth=1.5)
    tax.clear_matplotlib_ticks()
    
    st.pyplot(fig)
    st.success(f"**Klasifikasi:** {name} ({category})")
else:
    st.error("Total Q+F+L tidak boleh nol!")