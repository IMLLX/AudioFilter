from typing import Union, Optional, Tuple
import numpy as np
import scipy.signal as signal

FILTER_TYPES = ['highpass', 'lowpass', 'bandpass']


def fit_IIR_filter(
        audio: Union[str, np.ndarray],
        sample_rate: Union[int, float],
        b: int,
        a: int
) -> Tuple[np.ndarray, int]:
    filt_data = signal.filtfilt(b, a, audio, axis=0)
    return filt_data, sample_rate


def fit_FIR_filter(
        audio: Union[str, np.ndarray],
        sample_rate: Union[int, float],
        b: int,
) -> Tuple[np.ndarray, int]:
    filt_data = signal.filtfilt(b, 1, x=audio)
    return audio, sample_rate
