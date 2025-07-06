from flask import Flask, request, jsonify, render_template
import numpy as np
from scipy import signal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    rp = float(data['rp'])      # passband ripple (dB)
    Wn = float(data['wn'])      # cutoff frequency (normalized 0-1)
    N = int(data['order'])      # filter order

    b, a = signal.cheby1(N, rp, Wn, btype='low', analog=False)
    w, h = signal.freqz(b, a, worN=8000)
    freq = w / np.pi            # normalized frequency 0-1
    gain = 20 * np.log10(abs(h))

    return jsonify({'freq': freq.tolist(), 'gain': gain.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
