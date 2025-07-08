import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from chebyshevcalc import ChebyshevLowpass  # your class file

st.set_page_config(page_title="Chebyshev Filter Lab", layout="wide")

st.title("🧪 Chebyshev Lowpass Filter Designer")

# Sidebar controls
with st.sidebar:
    st.header("Filter Parameters")
    filter_type = st.selectbox("Filter Type", ["type1", "type2"])
    order = st.slider("Order", 1, 10, 5)
    cutoff = st.number_input("Cutoff Frequency (Hz)", value=1000.0)
    sample_rate = st.number_input("Sample Rate (Hz)", value=8000.0)

    if filter_type == "type1":
        ripple_db = st.slider("Passband Ripple (dB)", 0.1, 5.0, 0.5)
    else:
        stopband_atten = st.slider("Stopband Attenuation (dB)", 20.0, 100.0, 50.0)

    st.header("Plot Customization")
    marker_freqs = st.text_input("Frequency Markers (comma-separated Hz)", value="500, 1000, 2000")
    xlim = st.slider("X-axis Limits (Hz)", 10, int(sample_rate / 2), (10, int(sample_rate / 2)))
    ylim = st.slider("Y-axis Limits (dB)", -100, 10, (-80, 5))

# Parse marker frequencies
try:
    markers = [float(f.strip()) for f in marker_freqs.split(",") if f.strip()]
except ValueError:
    st.error("Invalid frequency marker input.")
    markers = []

# Design filter
designer = ChebyshevLowpass(filter_type)
if filter_type == "type1":
    b, a = designer.design_filter(order, cutoff, ripple_db=ripple_db, sample_rate=sample_rate)
else:
    b, a = designer.design_filter(order, cutoff, stopband_atten=stopband_atten, sample_rate=sample_rate)

w, h = designer.frequency_response(sample_rate=sample_rate)
magnitude_db = 20 * np.log10(abs(h))
phase_deg = np.angle(h) * 180 / np.pi

# Plot magnitude response
st.subheader("📈 Magnitude Response")
fig_mag, ax_mag = plt.subplots()
ax_mag.semilogx(w, magnitude_db, label="Magnitude")
for f in markers:
    ax_mag.axvline(f, color='red', linestyle='--', alpha=0.5, label=f"Marker: {f} Hz")
ax_mag.set_title("Magnitude Response (dB)")
ax_mag.set_xlabel("Frequency (Hz)")
ax_mag.set_ylabel("Magnitude (dB)")
ax_mag.set_xlim(*xlim)
ax_mag.set_ylim(*ylim)
ax_mag.grid(True, which='both', linestyle='--', alpha=0.4)
ax_mag.legend(loc='lower left', fontsize='small')
st.pyplot(fig_mag)

# Plot phase response
st.subheader("📉 Phase Response")
fig_phase, ax_phase = plt.subplots()
ax_phase.semilogx(w, phase_deg, label="Phase", color='orange')
for f in markers:
    ax_phase.axvline(f, color='red', linestyle='--', alpha=0.5)
ax_phase.set_title("Phase Response (degrees)")
ax_phase.set_xlabel("Frequency (Hz)")
ax_phase.set_ylabel("Phase (°)")
ax_phase.set_xlim(*xlim)
ax_phase.grid(True, which='both', linestyle='--', alpha=0.4)
st.pyplot(fig_phase)

# Pole-zero plot
st.subheader("🔁 Pole-Zero Diagram")
designer.get_poles_zeros()
fig_pz, ax_pz = plt.subplots()
theta = np.linspace(0, 2 * np.pi, 100)
ax_pz.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.4)
ax_pz.scatter(designer.poles.real, designer.poles.imag, c='r', marker='x', label='Poles')
ax_pz.scatter(designer.zeros.real, designer.zeros.imag, facecolors='none', edgecolors='b', label='Zeros')
ax_pz.set_xlabel("Real")
ax_pz.set_ylabel("Imaginary")
ax_pz.set_title("Pole-Zero Plot")
ax_pz.axis('equal')
ax_pz.grid(True, linestyle='--', alpha=0.3)
ax_pz.legend()
st.pyplot(fig_pz)

