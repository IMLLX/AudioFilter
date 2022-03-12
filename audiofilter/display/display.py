from typing import Union, Optional
from audiofilter.utils.contents import (
    DEFAULT_SAMPLE_RATE, DEFAULT_STFT_LEN
)
from audiofilter.audio.utils import validate_load_audio

from numpy.fft import (fft, fftfreq)
import numpy as np
import librosa.display
import scipy.signal as signal

pi = np.pi
tan = np.tan


def wave_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        ax1=None,
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    librosa.display.waveshow(audio, sr=sample_rate, ax=ax1)
    ax1.set_title('Time wave')
    ax1.set_ylabel('Amplitude [relative]')
    ax1.set_xlabel('Time [s]')


def freq_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        ax=None,
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    n_channels, sample_points = audio.ndim, audio.shape[0]
    audio_fft = fft(audio, axis=0) / sample_points
    freq = fftfreq(sample_points, 1.0 / sample_rate)
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
        stft_len: int = DEFAULT_STFT_LEN,
        ax=None
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    npers = stft_len * sample_rate / 1e3
    f, t, Zxx = signal.stft(audio, sample_rate, nperseg=npers)
    ax.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=0.1)
    ax.set_title('STFT Magnitude')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Frequency [Hz]')
