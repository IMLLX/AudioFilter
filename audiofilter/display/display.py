from typing import Union
from audiofilter.utils.contents import (
    DEFAULT_SAMPLE_RATE
)
from audiofilter.audio.utils import validate_load_audio
from numpy.fft import (
    fft, fftfreq
)

import matplotlib.pyplot as plt
import numpy as np
import librosa.display


def wave_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    librosa.display.waveshow(audio, sr=sample_rate)


def freq_plot(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
):
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    n_channels, sample_points = audio.ndim, len(audio.shape[-1])
    audio_fft = fft(audio, axis=0) / sample_points
    freq = fftfreq(sample_points, 1.0 / sample_rate)
    plt.plot(freq, audio_fft)
