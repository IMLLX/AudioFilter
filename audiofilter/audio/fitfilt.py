from typing import Union, Optional, Tuple
from numpy import tan, pi
from audiofilter.utils import (
    DEFAULT_N_LEVEL, DEFAULT_CUTOFF_HZ, DEFAULT_START_HZ
)

import audiofilter.audio.utils as audutils
import numpy as np
import scipy.signal as signal


def fit_highpass_filter(
        audio: Union[str, np.ndarray],
        sample_rate: Union[int, float],
        cutoff_hz: float = DEFAULT_CUTOFF_HZ,
        N: Optional[int] = DEFAULT_N_LEVEL,
        Rp: Optional[float] = None,
        As: Optional[float] = None,
        cutoff_hz2: Optional[float] = None
) -> Tuple[np.ndarray, int]:
    assert isinstance(cutoff_hz, (int, float)), "Expect 'cutoff_hz' to be a float"
    assert isinstance(N, int), "Expect 'N' to be an int"
    audio, sample_rate = audutils.validate_load_audio(audio, sample_rate)

    n_channels = audio.ndim

    T = 1. / sample_rate
    if Rp or As:
        assert isinstance(Rp, float) and isinstance(As, (int, float)), "Expect 'Rp' and 'As' to be an int or float"
        assert cutoff_hz2, "Expect 'cutoff_hz2' to be a float"

        wp, ws = 2 * pi * cutoff_hz / sample_rate, 2 * pi * cutoff_hz2 / sample_rate
        omega_p, omega_s = (2 / T) * tan(wp / 2), (2 / T) * tan(ws / 2)
        N, Wn = signal.buttord(omega_p, omega_s, Rp, As, False)

    else:
        Wn = 2 * cutoff_hz / sample_rate

    b, a = signal.butter(N, Wn, 'Highpass')
    filted_data = signal.filtfilt(b, a, audio, axis=0)
    return filted_data, sample_rate


def fit_lowpass_filter(
        audio: Union[str, np.ndarray],
        sample_rate: Union[int, float],
        cutoff_hz: float = DEFAULT_CUTOFF_HZ,
        N: Optional[int] = DEFAULT_N_LEVEL,
        Rp: Optional[float] = None,
        As: Optional[float] = None,
        cutoff_hz2: Optional[float] = None
) -> Tuple[np.ndarray, int]:
    assert isinstance(cutoff_hz, (int, float)), "Expect 'cutoff_hz' to be a float"
    assert isinstance(N, int), "Expect 'N' to be an int"
    audio, sample_rate = audutils.validate_load_audio(audio, sample_rate)

    n_channels = audio.ndim
    # audio.reshape(n_channels, -1)

    T = 1. / sample_rate
    if Rp or As:
        assert isinstance(Rp, float) and isinstance(As, (int, float)), "Expect 'Rp' and 'As' to be an int or float"
        assert cutoff_hz2, "Expect 'cutoff_hz2' to be a float"

        wp, ws = 2 * pi * cutoff_hz / sample_rate, 2 * pi * cutoff_hz2 / sample_rate
        omega_p, omega_s = (2 / T) * tan(wp / 2), (2 / T) * tan(ws / 2)
        N, Wn = signal.buttord(omega_p, omega_s, Rp, As, False)

    else:
        Wn = 2 * cutoff_hz / sample_rate

    b, a = signal.butter(N, Wn, 'lowpass')
    filted_data = signal.filtfilt(b, a, audio, axis=0)
    return filted_data, sample_rate


def fit_band_filter(
        audio: Union[str, np.ndarray],
        sample_rate: Union[int, float],
        start_hz: float = DEFAULT_START_HZ,
        cutoff_hz: float = DEFAULT_CUTOFF_HZ,
        N: Optional[int] = DEFAULT_N_LEVEL,
        Rp: Optional[float] = None,
        As: Optional[float] = None,
        cutoff_hz2: Optional[float] = None
) -> Tuple[np.ndarray, int]:
    Wn1 = 2 * cutoff_hz / sample_rate
    Wn2 = 2 * start_hz / sample_rate
    b, a = signal.butter(N, [Wn1, Wn2], 'bandpass')
    filt_data = signal.filtfilt(b, a, audio, axis=0)
    return filt_data, sample_rate
