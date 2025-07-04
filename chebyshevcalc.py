# recreating the chebyshev approximation in python 
#label all the variables
# low vs high
# G_n os a function of angular frequency omega of the nth-order 


import numpy as np
import matplotlib as plt
from scipy import signal
import math

class ChebyshevLowpass:
    """
    Generalized Chebyshev Lowpass Filter Designer
    Supports both Type I and Type II Chebyshev approximations
    """
    
    def __init__(self, filter_type='type1'):
        """
        Initialize the Chebyshev filter designer
        
        Args:
            filter_type: 'type1' or 'type2' for Chebyshev Type I or Type II
        """
        self.filter_type = filter_type
        self.coefficients = None
        self.poles = None
        self.zeros = None
        
    def design_filter(self, order, cutoff_freq, ripple_db=1.0, stopband_atten=40.0, 
                     sample_rate=None):
        """
        Design the Chebyshev lowpass filter
        
        Args:
            order: Filter order (integer)
            cutoff_freq: Cutoff frequency (Hz if sample_rate given, else normalized)
            ripple_db: Passband ripple in dB (Type I) or stopband ripple (Type II)
            stopband_atten: Stopband attenuation in dB (Type II only)
            sample_rate: Sampling rate in Hz (None for analog filter)
        
        Returns:
            b, a: Numerator and denominator coefficients
        """
        
        if sample_rate is not None:
            # Digital filter design
            nyquist = sample_rate / 2
            normalized_cutoff = cutoff_freq / nyquist
            
            if self.filter_type == 'type1':
                b, a = signal.cheby1(order, ripple_db, normalized_cutoff, 
                                   btype='low', analog=False)
            else:  # type2
                b, a = signal.cheby2(order, stopband_atten, normalized_cutoff, 
                                   btype='low', analog=False)
        else:
            # Analog filter design
            if self.filter_type == 'type1':
                b, a = signal.cheby1(order, ripple_db, cutoff_freq, 
                                   btype='low', analog=True)
            else:  # type2
                b, a = signal.cheby2(order, stopband_atten, cutoff_freq, 
                                   btype='low', analog=True)
        
        self.coefficients = (b, a)
        return b, a
    
    def get_poles_zeros(self):
        """
        Extract poles and zeros from the designed filter
        
        Returns:
            poles, zeros: Arrays of pole and zero locations
        """
        if self.coefficients is None:
            raise ValueError("Filter must be designed first")
        
        b, a = self.coefficients
        zeros = np.roots(b)
        poles = np.roots(a)
        
        self.poles = poles
        self.zeros = zeros
        
        return poles, zeros
    
    def frequency_response(self, frequencies=None, sample_rate=None):
        """
        Calculate the frequency response of the designed filter
        
        Args:
            frequencies: Array of frequencies to evaluate (optional)
            sample_rate: Sampling rate for digital filters
        
        Returns:
            w: Frequency array
            h: Complex frequency response
        """
        if self.coefficients is None:
            raise ValueError("Filter must be designed first")
        
        b, a = self.coefficients
        
        if sample_rate is not None:
            # Digital filter
            if frequencies is None:
                w, h = signal.freqz(b, a, worN=1024)
                w = w * sample_rate / (2 * np.pi)
            else:
                w, h = signal.freqz(b, a, worN=frequencies * 2 * np.pi / sample_rate)
        else:
            # Analog filter
            if frequencies is None:
                w, h = signal.freqs(b, a, worN=1024)
            else:
                w, h = signal.freqs(b, a, worN=frequencies)
        
        return w, h
    
    def plot_response(self, sample_rate=None, title=None):
        """
        Plot the magnitude and phase response of the filter
        
        Args:
            sample_rate: Sampling rate for digital filters
            title: Custom title for the plot
        """
        if self.coefficients is None:
            raise ValueError("Filter must be designed first")
        
        w, h = self.frequency_response(sample_rate=sample_rate)
        
        # Convert to dB
        magnitude_db = 20 * np.log10(abs(h))
        phase_deg = np.angle(h) * 180 / np.pi
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Magnitude response
        ax1.semilogx(w, magnitude_db)
        ax1.set_title(title or f'Chebyshev {self.filter_type.upper()} Lowpass Filter Response')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Magnitude (dB)')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(-80, 5)
        
        # Phase response
        ax2.semilogx(w, phase_deg)
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (degrees)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_pole_zero(self):
        """
        Plot the pole-zero diagram
        """
        if self.poles is None or self.zeros is None:
            self.get_poles_zeros()
        
        plt.figure(figsize=(8, 8))
        
        # Plot unit circle for reference (digital filters)
        theta = np.linspace(0, 2*np.pi, 100)
        plt.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5, label='Unit Circle')
        
        # Plot poles and zeros
        plt.scatter(self.poles.real, self.poles.imag, marker='x', s=100, 
                   c='red', linewidth=3, label='Poles')
        if len(self.zeros) > 0:
            plt.scatter(self.zeros.real, self.zeros.imag, marker='o', s=100, 
                       facecolors='none', edgecolors='blue', linewidth=2, label='Zeros')
        
        plt.xlabel('Real Part')
        plt.ylabel('Imaginary Part')
        plt.title(f'Pole-Zero Plot - Chebyshev {self.filter_type.upper()}')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.legend()
        plt.show()


### Testing
def main():
    """
    Example usage of the Chebyshev lowpass filter designer
    """
    print("=== Chebyshev Lowpass Filter Designer ===\n")
    
    # Example 1: Digital Chebyshev Type I filter
    print("1. Digital Chebyshev Type I Filter:")
    cheby1 = ChebyshevLowpass('type1')
    
    # Design parameters
    order = 5
    cutoff_freq = 1000  # Hz
    ripple_db = 0.5     # dB
    sample_rate = 8000  # Hz
    
    b1, a1 = cheby1.design_filter(order, cutoff_freq, ripple_db, 
                                 sample_rate=sample_rate)
    
    print(f"Order: {order}")
    print(f"Cutoff frequency: {cutoff_freq} Hz")
    print(f"Passband ripple: {ripple_db} dB")
    print(f"Sampling rate: {sample_rate} Hz")
    print(f"Numerator coefficients: {b1}")
    print(f"Denominator coefficients: {a1}\n")
    
    # Example 2: Digital Chebyshev Type II filter
    print("2. Digital Chebyshev Type II Filter:")
    cheby2 = ChebyshevLowpass('type2')
    
    stopband_atten = 50  # dB
    
    b2, a2 = cheby2.design_filter(order, cutoff_freq, stopband_atten=stopband_atten,
                                 sample_rate=sample_rate)
    
    print(f"Order: {order}")
    print(f"Cutoff frequency: {cutoff_freq} Hz")
    print(f"Stopband attenuation: {stopband_atten} dB")
    print(f"Sampling rate: {sample_rate} Hz")
    print(f"Numerator coefficients: {b2}")
    print(f"Denominator coefficients: {a2}\n")
    
    # Plot responses
    print("Plotting frequency responses...")
    cheby1.plot_response(sample_rate=sample_rate, 
                        title="Chebyshev Type I Lowpass Filter")
    cheby2.plot_response(sample_rate=sample_rate, 
                        title="Chebyshev Type II Lowpass Filter")
    
    # Plot pole-zero diagrams
    print("Plotting pole-zero diagrams...")
    cheby1.plot_pole_zero()
    cheby2.plot_pole_zero()
    
    # Example 3: Analog filter design
    print("3. Analog Chebyshev Type I Filter:")
    cheby_analog = ChebyshevLowpass('type1')
    
    analog_cutoff = 2 * np.pi * 1000  # rad/s
    b_analog, a_analog = cheby_analog.design_filter(order, analog_cutoff, ripple_db)
    
    print(f"Analog cutoff frequency: {analog_cutoff/(2*np.pi)} Hz")
    print(f"Numerator coefficients: {b_analog}")
    print(f"Denominator coefficients: {a_analog}")
    
    # Calculate some key parameters
    print("\n=== Filter Analysis ===")
    
    # Get poles and zeros
    poles1, zeros1 = cheby1.get_poles_zeros()
    print(f"Type I - Number of poles: {len(poles1)}, Number of zeros: {len(zeros1)}")
    
    poles2, zeros2 = cheby2.get_poles_zeros()
    print(f"Type II - Number of poles: {len(poles2)}, Number of zeros: {len(zeros2)}")


if __name__ == "__main__":
    main()