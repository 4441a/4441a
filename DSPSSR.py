# furui_dsp_library.py (revised)
# A Python library inspired by Sadao Furui's "Digital Speech Processing, Synthesis, and Recognition"
# Implements key algorithms and functions for educational purposes.
# Requires: numpy, scipy (both standard in most environments)
# Revisions: Removed HMM function due to dependency on unavailable 'hmmlearn'; minor docstring enhancements; added zero-check in pitch detection.

import numpy as np
from scipy.signal import lfilter, resample
from scipy.linalg import toeplitz

def speech_production_model(amplitude=1.0, frequency=100, duration=1.0, fs=16000):
    """
    Simple speech production model simulation (e.g., glottal pulse approximation).
    Based on Chapter 2: Speech Production Models.
    Generates a basic voiced sound waveform.
    
    Args:
        amplitude (float): Signal amplitude.
        frequency (float): Fundamental frequency (pitch).
        duration (float): Duration in seconds.
        fs (int): Sampling frequency.
    
    Returns:
        np.ndarray: Simulated speech waveform.
    """
    t = np.linspace(0, duration, int(fs * duration))
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    return waveform

def pitch_detection_autocorr(signal, fs=16000, min_freq=80, max_freq=300):
    """
    Basic pitch detection using autocorrelation.
    Based on Chapter 2: Characteristics of Speech Signals.
    Finds fundamental frequency (pitch) for voiced segments.
    
    Args:
        signal (np.ndarray): Input speech frame.
        fs (int): Sampling frequency.
        min_freq (float): Minimum expected pitch (Hz).
        max_freq (float): Maximum expected pitch (Hz).
    
    Returns:
        float: Estimated pitch frequency, or 0 if unvoiced.
    """
    autocorr = np.correlate(signal, signal, mode='full')[len(signal):]
    max_auto = np.max(autocorr)
    if max_auto == 0:
        return 0.0
    autocorr = autocorr / max_auto  # Normalize
    min_lag = int(fs / max_freq)
    max_lag = int(fs / min_freq)
    peak_lag = np.argmax(autocorr[min_lag:max_lag]) + min_lag
    if autocorr[peak_lag] < 0.5:  # Threshold for voiced/unvoiced
        return 0.0
    return fs / peak_lag

def lpc_analysis(signal, order=12, preemphasis=0.97):
    """
    Linear Predictive Coding (LPC) analysis.
    Based on Chapter 4: Linear Predictive Coding (LPC).
    Computes LPC coefficients using autocorrelation and Levinson-Durbin recursion.
    
    Args:
        signal (np.ndarray): Input speech frame (e.g., windowed segment).
        order (int): LPC order (number of coefficients).
        preemphasis (float): Pre-emphasis factor (set to 0 to disable).
    
    Returns:
        np.ndarray: LPC coefficients.
    """
    if preemphasis > 0:
        signal = np.append(signal[0], signal[1:] - preemphasis * signal[:-1])
    
    # Autocorrelation
    autocorr = np.correlate(signal, signal, mode='full')[len(signal)-1:]
    R = toeplitz(autocorr[:order])
    r = autocorr[1:order+1]
    
    # Levinson-Durbin recursion (via matrix solve)
    a = np.linalg.solve(R, r)
    a = np.insert(-a, 0, 1.0)  # Include a0 = 1
    return a

def lpc_synthesis(excitation, lpc_coeffs, gain=1.0):
    """
    LPC-based speech synthesis (analysis-synthesis method).
    Based on Chapter 3: Speech Analysis and Analysis-Synthesis Systems.
    Reconstructs signal using LPC filter on excitation source.
    
    Args:
        excitation (np.ndarray): Excitation signal (e.g., noise for unvoiced, pulse for voiced).
        lpc_coeffs (np.ndarray): LPC coefficients.
        gain (float): Gain factor.
    
    Returns:
        np.ndarray: Synthesized speech signal.
    """
    synthesized = gain * lfilter([1], lpc_coeffs, excitation)
    return synthesized

def waveform_coding_synthesis(original_signal, bit_rate_reduction_factor=2):
    """
    Basic waveform coding for synthesis.
    Based on Chapter 7: Synthesis Based on Waveform Coding.
    Simplifies by downsampling and upsampling (e.g., ADPCM-like approximation).
    
    Args:
        original_signal (np.ndarray): Input waveform.
        bit_rate_reduction_factor (int): Factor for reducing sample rate (simulates compression).
    
    Returns:
        np.ndarray: Reconstructed waveform.
    """
    downsampled = resample(original_signal, len(original_signal) // bit_rate_reduction_factor)
    reconstructed = resample(downsampled, len(original_signal))
    return reconstructed

def cepstral_analysis(signal, n_ceps=13):
    """
    Cepstral analysis for feature extraction (used in recognition).
    Based on recognition chapters (e.g., MFCC-like, but simplified homomorphic cepstrum).
    
    Args:
        signal (np.ndarray): Input speech frame.
        n_ceps (int): Number of cepstral coefficients.
    
    Returns:
        np.ndarray: Cepstral coefficients.
    """
    spectrum = np.fft.fft(signal)
    log_spectrum = np.log(np.abs(spectrum) + 1e-10)
    cepstrum = np.fft.ifft(log_spectrum).real
    return cepstrum[:n_ceps]

def train_vq_codebook(features, codebook_size=256, max_iter=100, tol=1e-4):
    """
    Basic Vector Quantization (VQ) codebook training using k-means-like algorithm.
    Based on Appendix C: Vector Quantization Algorithm.
    Trains a codebook from feature vectors.
    
    Args:
        features (np.ndarray): Feature vectors (M x D array).
        codebook_size (int): Number of codebook entries.
        max_iter (int): Maximum iterations.
        tol (float): Convergence tolerance.
    
    Returns:
        np.ndarray: Trained codebook (codebook_size x D).
    """
    codebook = features[np.random.choice(len(features), codebook_size, replace=False)]
    for _ in range(max_iter):
        distances = np.linalg.norm(features[:, np.newaxis] - codebook, axis=2)
        labels = np.argmin(distances, axis=1)
        new_codebook = np.array([features[labels == k].mean(axis=0) if np.sum(labels == k) > 0 else codebook[k] for k in range(codebook_size)])
        if np.linalg.norm(new_codebook - codebook) < tol:
            break
        codebook = new_codebook
    return codebook

def vector_quantization(codebook, features):
    """
    Vector Quantization (VQ) for compression/recognition.
    Based on Appendix C: Vector Quantization Algorithm.
    Finds nearest codebook entry for each feature vector.
    
    Args:
        codebook (np.ndarray): Pre-trained codebook (N x D array).
        features (np.ndarray): Feature vectors (M x D array).
    
    Returns:
        np.ndarray: Quantized indices.
    """
    distances = np.linalg.norm(features[:, np.newaxis] - codebook, axis=2)
    indices = np.argmin(distances, axis=1)
    return indices

# Example usage (commented out):
# if __name__ == "__main__":
#     fs = 16000
#     signal = speech_production_model(frequency=120, duration=0.1, fs=fs)
#     pitch = pitch_detection_autocorr(signal, fs=fs)
#     print("Estimated pitch:", pitch)
#     lpc_coeffs = lpc_analysis(signal)
#     synthesized = lpc_synthesis(np.random.randn(len(signal)), lpc_coeffs)
#     print("Synthesized signal:", synthesized[:10])
#     features = np.random.randn(100, 13)  # Dummy cepstral features
#     codebook = train_vq_codebook(features, codebook_size=8)
#     indices = vector_quantization(codebook, features)
#     print("VQ indices:", indices[:5])