# streamlit_app.py
import streamlit as st
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from chebyshevcalc import ChebyshevLowpass  # or just copy-paste your class here

st.title("🧪 Interactive Chebyshev Lowpass Filter Designer")

# Sidebar inputs
filter_type = st.sidebar.selectbox("Filter Type", ["type1", "type2"])
order = st.sidebar.slider("Filter Order", min_value=1, max_value=10, value=5)
cutoff_freq = st.sidebar.number_input("Cutoff Frequency (Hz)", value=1000)
sample_rate = st.sidebar.number_input("Sampling Rate (Hz)", value=8000)

if filter_type == "type1":
    ripple_db = st.sidebar.slider("Passband Ripple (dB)", 0.1, 5.0, 0.5)
else:
    stopband_atten = st.sidebar.slider("Stopband Attenuation (dB)", 20.0, 100.0, 50.0)

# Design filter
designer = ChebyshevLowpass(filter_type)
if filter_type == "type1":
    b, a = designer.design_filter(order, cutoff_freq, ripple_db=ripple_db, sample_rate=sample_rate)
else:
    b, a = designer.design_filter(order, cutoff_freq, stopband_atten=stopband_atten, sample_rate=sample_rate)

# Plot frequency response
w, h = designer.frequency_response(sample_rate=sample_rate)
magnitude_db = 20 * np.log10(abs(h))

st.subheader("📈 Frequency Response")
fig1, ax1 = plt.subplots()
ax1.semilogx(w, magnitude_db)
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Magnitude (dB)")
ax1.set_title("Magnitude Response")
ax1.grid(True)
st.pyplot(fig1)

# Plot pole-zero
designer.get_poles_zeros()
st.subheader("🔁 Pole-Zero Plot")
fig2, ax2 = plt.subplots()
theta = np.linspace(0, 2*np.pi, 100)
ax2.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5)
ax2.scatter(designer.poles.real, designer.poles.imag, c='r', marker='x', label='Poles')
ax2.scatter(designer.zeros.real, designer.zeros.imag, facecolors='none', edgecolors='b', label='Zeros')
ax2.set_xlabel("Real")
ax2.set_ylabel("Imaginary")
ax2.set_title("Pole-Zero Diagram")
ax2.grid(True)
ax2.axis('equal')
ax2.legend()
st.pyplot(fig2)
