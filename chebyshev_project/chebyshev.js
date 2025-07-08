// chebyshev.js
export function cheby1Design(order, rippleDb, cutoffNorm) {
  // Pre-warp, ripple, etc. For brevity, use Butterworth → replace with full Chebyshev logic
  const rp = rippleDb;
  const eps = Math.sqrt(Math.pow(10, rp / 10) - 1);
  const sinhArg = Math.asinh(1 / eps) / order;
  const a = Math.sinh(sinhArg);
  const b = Math.cosh(sinhArg);

  const poles = [];
  for (let k = 1; k <= order; k++) {
    const theta = Math.PI * (2*k - 1) / (2 * order);
    const re = -a * Math.sin(theta);
    const im = b * Math.cos(theta);
    poles.push({ re, im });
  }

  // Convert to digital via bilinear transform
  const zPoles = poles.map(p => {
    const denom = 1 + p.re + (p.re * p.re + p.im * p.im) / 4;
    return {
      re: (1 - p.re + (p.re * p.re + p.im * p.im) / 4) / denom,
      im: (-p.im) / denom
    };
  });

  return { eps, poles: zPoles };
}

export function freqResponse(b, a, sampleRateHz=8000) {
  const n = 512;
  const w = [];
  const h = [];
  for (let i = 0; i < n; i++) {
    const omega = Math.PI * i / (n - 1);
    let num = { re: 0, im: 0 }, den = { re: 0, im: 0 };
    const z = { re: Math.cos(omega), im: Math.sin(omega) };
    for (let k = 0; k < b.length; k++) {
      // num += b[k] * z^-k
    }
    for (let k = 0; k < a.length; k++) {
      // den += a[k] * z^-k
    }
    w.push(omega * sampleRateHz / (2 * Math.PI));
    h.push(Math.sqrt((num.re*num.re + num.im*num.im) / (den.re*den.re + den.im*den.im)));
  }
  return { freqHz: w, mag: h };
}
