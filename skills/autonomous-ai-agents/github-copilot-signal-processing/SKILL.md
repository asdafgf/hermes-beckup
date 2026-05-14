---
name: github-copilot-signal-processing
description: "GitHub Copilot ile Python ve kütüphaneler kullanarak sinyal işleme (Signal Processing). Copilot'un mühendislik çalışmalarında nasıl kullanılacağı: numpy, scipy, matplotlib ile sinyal analizi, filtreleme, FFT, spektral analiz. AI-assisted mühendislik hesaplamaları."
version: 1.0
author: hermes
source: "https://www.youtube.com/live/ZM43F2tr41c — Copilot ile Sohbetler #6"
category: autonomous-ai-agents
tags: [github-copilot, signal-processing, python, numpy, scipy, engineering, ai-assisted]
---

# GitHub Copilot ile Python Sinyal İşleme

## 🎯 Ne Zaman Kullanılır

- Kullanıcı "Copilot ile mühendislik hesaplaması" dediğinde
- Python'da sinyal işleme, FFT, filtreleme konuşulduğunda
- AI-assisted mühendislik çalışmaları hakkında soru geldiğinde
- numpy/scipy/matplotlib ile sinyal analizi yapılırken

---

## 🧠 GitHub Copilot ile Mühendislik

GitHub Copilot, sadece web geliştirme için değil — **mühendislik hesaplamaları** için de güçlü bir araçtır.

### Copilot'un Mühendislikte Gücü
- Matematiksel formülleri koda çevirme
- Karmaşık kütüphane API'lerini hatırlama
- Tekrar eden hesaplama şablonlarını otomatik tamamlama
- Hata ayıklama ve optimizasyon önerileri

---

## 🔧 Python Sinyal İşleme Stack'i

| Kütüphane | Kullanım |
|-----------|----------|
| **NumPy** | Dizi işlemleri, FFT, matematiksel işlemler |
| **SciPy** | Filtre tasarımı, sinyal işleme fonksiyonları |
| **Matplotlib** | Sinyal görselleştirme, spektrum çizimleri |
| **PyTorch/TensorFlow** | Derin öğrenme tabanlı sinyal işleme |

---

## 💡 Copilot ile Sinyal İşleme Örnekleri

### 1. FFT (Hızlı Fourier Dönüşümü)
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Örnek sinyal oluştur
fs = 1000  # Örnekleme frekansı
t = np.arange(0, 1, 1/fs)
freq = 50  # 50 Hz sinyal
signal = np.sin(2 * np.pi * freq * t)

# FFT hesapla
N = len(signal)  # Copilot bunu otomatik tamamlar
yf = fft(signal)
xf = fftfreq(N, 1/fs)
```

### 2. Filtre Tasarımı
```python
from scipy import signal

# Butterworth filtre tasarımı
b, a = signal.butter(4, 100, 'low', fs=1000)  # 4. derece alçak geçiren
filtered = signal.filtfilt(b, a, raw_signal)
```

### 3. Spektral Analiz
```python
from scipy import signal as sp

# Spektrogram hesapla
f, t, Sxx = sp.spectrogram(signal, fs)
plt.pcolormesh(t, f, 10 * np.log10(Sxx))
plt.ylabel('Frekans [Hz]')
plt.xlabel('Zaman [sn]')
plt.colorbar(label='Güç [dB]')
```

---

## ⚡ Copilot İpuçları (Mühendislik İçin)

| İpucu | Açıklama |
|-------|----------|
| **Açıklayıcı yorum yaz** | "# FFT hesapla ve frekans spektrumunu çiz" gibi |
| **Kütüphane import'larını belirt** | "import numpy as np" yaz, Copilot devamını getirir |
| **Formülü yorum satırına yaz** | Copilot formülü koda çevirir |
| **Değişken isimlerini anlamlı ver** | `sampling_rate`, `cutoff_freq` gibi |

---

## 🔗 İlgili Skill'ler
- hermes-agent-comparison-guide — Agent karşılaştırması
- claude-ai-cheat-codes-levels — AI kullanım seviyeleri
