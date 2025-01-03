import librosa
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # یا 'Agg' برای جلوگیری از مشکلات گرافیکی
import matplotlib.pyplot as plt
import sounddevice as sd  # کتابخانه برای پخش فایل صوتی
import scipy.signal as signal
import soundfile as sf  # کتابخانه برای ذخیره فایل‌های صوتی

# بارگذاری یک فایل صوتی نمونه از کتابخانه librosa
audio, sr = librosa.load(librosa.example('trumpet'), sr=None)

# افزودن نویز به فایل صوتی با سطح نویز بالاتر
def add_noise(audio, noise_level=0.1):  # سطح نویز افزایش یافته
    noise = noise_level * np.random.randn(len(audio))
    return audio + noise

noisy_audio = add_noise(audio)

# کاهش نویز با استفاده از فیلتر پایین‌گذر
def reduce_noise(audio, sr, cutoff=3000):
    nyquist = 0.5 * sr  # فرکانس نیکوایست
    normal_cutoff = cutoff / nyquist  # نرمال‌سازی بر اساس فرکانس نیکوایست
    b, a = signal.butter(6, normal_cutoff, btype='low', analog=False)  # طراحی فیلتر
    return signal.filtfilt(b, a, audio)  # اعمال فیلتر روی سیگنال صوتی

denoised_audio = reduce_noise(noisy_audio, sr)

# تغییر گام و سرعت صدا
def change_pitch_speed(audio, sr, pitch_factor):
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_factor)  # تغییر گام

pitch_adjusted_audio = change_pitch_speed(denoised_audio, sr, 4)

# ذخیره فایل‌های صوتی پردازش شده
sf.write('denoised_audio.wav', denoised_audio, sr)
sf.write('pitch_adjusted_audio.wav', pitch_adjusted_audio, sr)

# پخش صدا
sd.play(denoised_audio, sr)
sd.wait()  # منتظر می‌مانیم تا پخش صدا تمام شود

# رسم نمودارها
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(audio[:5000])  # نمایش 5000 نمونه اول از صدای اصلی
plt.title('Original Audio')  # عنوان برای صدای اصلی
plt.subplot(3, 1, 2)
plt.plot(noisy_audio[:5000])  # نمایش 5000 نمونه اول از صدای نویزی
plt.title('Noisy Audio')  # عنوان برای صدای نویزی
plt.subplot(3, 1, 3)
plt.plot(denoised_audio[:5000])  # نمایش 5000 نمونه اول از صدای کاهش یافته از نویز
plt.title('Denoised Audio')  # عنوان برای صدای کاهش نویز شده
plt.tight_layout()  # تنظیم فاصله‌ها بین زیرنمودارها
plt.show()  # نمایش نمودارها
