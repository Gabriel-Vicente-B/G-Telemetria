import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Load the data from the file
file_path = 'Tensão_A.txt'

# Open and read the file, handling the comma-separated format
with open(file_path, 'r') as file:
    data = file.read().replace('\n', ',').split(',')

# Filter out any empty strings
data = [value for value in data if value.strip()]

# Convert the data to a numpy array of floats
data = np.array(data, dtype=np.float64)
data = data - np.mean(data)
# Sampling rate
sampling_rate = 1666  # Hz

# Calculate the FFT
n = len(data)
yf = np.fft.fft(data)
xf = np.fft.fftfreq(n, 1 / sampling_rate)

# Find the peak frequency
idx = np.argmax(np.abs(yf))
dominant_frequency = np.abs(xf[idx])

# Print the dominant frequency
print(f"Dominant frequency: {dominant_frequency} Hz")

# Plot the signal and its frequency domain
plt.figure(figsize=(12, 6))

# Time-domain plot
plt.subplot(2, 1, 1)
time = np.arange(0, n) / sampling_rate
plt.plot(time, data)
plt.title("Time Domain Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Frequency-domain plot
plt.subplot(2, 1, 2)
plt.plot(xf[:n // 2], np.abs(yf[:n // 2]))
plt.title("Frequency Domain Signal")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.grid()

plt.tight_layout()
plt.show()