import librosa
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' to avoid graphical issues
import matplotlib.pyplot as plt
import sounddevice as sd  # Library for audio playback
import scipy.signal as signal
import soundfile as sf  # Library for saving audio files

# Load a sample audio file from librosa
audio, sr = librosa.load(librosa.example('trumpet'), sr=None)

# Add noise to the audio with a higher noise level
def add_noise(audio, noise_level=0.1):  # Increased noise level
    noise = noise_level * np.random.randn(len(audio))
    return audio + noise

noisy_audio = add_noise(audio)

# Reduce noise using a low-pass filter
def reduce_noise(audio, sr, cutoff=3000):
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(6, normal_cutoff, btype='low', analog=False)
    return signal.filtfilt(b, a, audio)

denoised_audio = reduce_noise(noisy_audio, sr)

# Change pitch and speed
def change_pitch_speed(audio, sr, pitch_factor):
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_factor)

pitch_adjusted_audio = change_pitch_speed(denoised_audio, sr, 4)

# Save the processed audio
sf.write('denoised_audio.wav', denoised_audio, sr)
sf.write('pitch_adjusted_audio.wav', pitch_adjusted_audio, sr)

# Play the audio
sd.play(denoised_audio, sr)
sd.wait()  # Wait until the audio playback is finished

# Visualization
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(audio[:5000])
plt.title('Original Audio')
plt.subplot(3, 1, 2)
plt.plot(noisy_audio[:5000])
plt.title('Noisy Audio')
plt.subplot(3, 1, 3)
plt.plot(denoised_audio[:5000])
plt.title('Denoised Audio')
plt.tight_layout()
plt.show()
