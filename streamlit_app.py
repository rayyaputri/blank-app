import streamlit as st
import matplotlib.pyplot as plt
import ternary

# Konfigurasi Halaman
st.set_page_config(page_title="Pettijohn Classifier", layout="centered")

st.title("💎 Klasifikasi Batuan Sedimen (Pettijohn, 1975)")
st.write("Masukkan persentase mineral dan matriks untuk memulai klasifikasi.")

# --- STEP 1: INPUT DATA (Default Set ke 0.0) ---
col1, col2 = st.columns(2)
with col1:
    q = st.number_input("Quartz (%)", min_value=0.0, max_value=100.0, value=0.0)
    f = st.number_input("Feldspar (%)", min_value=0.0, max_value=100.0, value=0.0)
with col2:
    l = st.number_input("Lithic Fragments (%)", min_value=0.0, max_value=100.0, value=0.0)
    m = st.number_input("Matrix (%)", min_value=0.0, max_value=100.0, value=0.0)

# --- STEP 2: TOMBOL PROSES ---
if st.button("Classify & Plot Diagram"):
    total = q + f + l
    
    if total == 0:
        st.error("Total Q+F+L tidak boleh nol. Silakan masukkan angka.")
    else:
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

        # --- STEP 3: PLOTTING ---
        fig, tax = ternary.figure(scale=100)
        fig.set_size_inches(8, 7)

        # Garis Pembagi
        tax.line((0, 95, 5), (5, 95, 0), linewidth=1.5, color='black')
        tax.line((0, 75, 25), (25, 75, 0), linewidth=1.5, color='black')
        tax.line((0, 100, 0), (50, 0, 50), linewidth=1.5, color='black')

        # Titik Sampel (L, Q, F)
        tax.scatter([(L, Q, F)], marker='o', color='yellow', s=200, edgecolors='black', zorder=10)

        # Label Sudut
        ax = tax.get_axes()
        ax.text(50, 103, "QUARTZ (Q)", fontsize=10, fontweight='bold', ha='center')
        ax.text(-12, -5, "FELDSPAR (F)", fontsize=10, fontweight='bold', ha='center')
        ax.text(112, -5, "LITHIC (L)", fontsize=10, fontweight='bold', ha='center')

        tax.boundary(linewidth=2)
        tax.clear_matplotlib_ticks()
        ax.axis('off')
        
        # Tampilkan Hasil di Web
        st.pyplot(fig)
        st.success(f"**Hasil Klasifikasi:** {name} ({category})")
        st.info(f"Normalisasi QFL: Q={Q:.1f}%, F={F:.1f}%, L={L:.1f}%")