from typing import Union, Optional
from audiofilter.utils.contents import (
    DEFAULT_SAMPLE_RATE, DEFAULT_STFT_LEN
)
from audiofilter.audio.utils import validate_load_audio
from numpy.fft import (fft, fftfreq)
from matplotlib import patches
from matplotlib.pyplot import axvline, axhline

import numpy as np
import librosa.display
import scipy.signal as signal

pi = np.pi
tan = np.tan


def wave_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        ax1=None,
        cla: bool = False
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    if cla:
        ax1.cla()
    librosa.display.waveshow(audio, sr=sample_rate, ax=ax1)
    ax1.set_title('Time wave')
    ax1.set_ylabel('Amplitude [relative]')
    ax1.set_xlabel('Time [s]')


def freq_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        ax=None,
        cla: bool = False
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    n_channels, sample_points = audio.ndim, audio.shape[0]
    audio_fft = fft(audio, axis=0) / sample_points
    freq = fftfreq(sample_points, 1.0 / sample_rate)
    if cla:
        ax.cla()
    ax.plot(freq, abs(audio_fft))
    ax.set_title('Frequency response')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitude [relative]')


def display_plt(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        axes=None
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    wave_plot(audio, sample_rate, axes[0])
    freq_plot(audio, sample_rate, axes[1])


def STFT_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        window_type=None,
        stft_len: int = DEFAULT_STFT_LEN,
        ax=None
):
    npers = stft_len * sample_rate / 1e3
    f, t, Zxx = signal.stft(audio, sample_rate, window_type, nperseg=npers)
    ax.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=.1, shading='auto')
    ax.set_title('STFT Magnitude')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Frequency [Hz]')


def display_zero_pole(b, a, ax):
    zeros, poles, k = signal.tf2zpk(b, a)
    unit_circle = patches.Circle((0, 0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.1)
    ax.axvline(0, color='0.7')
    ax.axhline(0, color='0.7')
    ax.add_patch(unit_circle)
    ax.plot(poles.real, poles.imag, 'x', markersize=9, alpha=0.5, color='blue')
    ax.plot(zeros.real, zeros.imag, 'o', markersize=9, alpha=0.5, color='blue')
    ax.set_xlim((-2, 2))
    ax.set_xlabel('Real')
    ax.set_ylim((-1.5, 1.5))
    ax.set_ylabel('Imag')


def display_angle_plot(f, h, ax):
    ax.plot(f, np.angle(h))
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Angle [rad]')
