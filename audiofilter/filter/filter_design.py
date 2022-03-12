from typing import Optional, Union, Any
from .content import (
    DEFAULT_RP, DEFAULT_AS, DEFAULT_N_VALUE
)
import numpy as np
import scipy.signal as signal

pi = np.pi
tan = np.tan


def IIR_filter_design(
        sample_rate: Union[int, float],
        filter_type: str,
        irr_type: str,
        fp1: float,
        fst1: float,
        fp2: Optional[float] = None,
        fst2: Optional[float] = None,
        Rp: Optional[float] = DEFAULT_RP,
        As: Optional[float] = DEFAULT_AS,
):
    Fs = sample_rate
    T = 1 / Fs
    wp = 2 * pi * fp1 / Fs
    ws = 2 * pi * fst1 / Fs

    omega_p = (2 / T) * tan(wp / 2)
    omega_s = (2 / T) * tan(ws / 2)
    if irr_type == 'butter':
        N, Wn = signal.buttord(omega_p, omega_s, Rp, As, True)
        b, a = signal.butter(N, Wn, filter_type, analog=True)
    elif irr_type == 'chebyI':
        N, Wn = signal.cheb1ord(omega_p, omega_s, Rp, As, True)
        b, a = signal.cheby1(N, Rp, Wn, filter_type, analog=True)
    elif irr_type == 'chebyII':
        N, Wn = signal.cheb2ord(omega_p, omega_s, Rp, As, True)
        b, a = signal.cheby2(N, As, Wn, filter_type, analog=True)
    else:
        N, Wn = signal.ellipord(omega_p, omega_s, Rp, As, True)
        b, a = signal.ellip(N, Rp, As, Wn, filter_type, analog=True)
    if N > 30:
        raise Exception("Too Large N the filter might be meaningless")
    b_dig, a_dig = signal.bilinear(b, a, fs=Fs)

    return b_dig, a_dig


def FIR_filter_design(
        sample_rate: Union[int, float],
        win_type: str,
        fp1: float,
        fst1: float,
        fp2: Optional[float] = None,
        fst2: Optional[float] = None,
        N: int = DEFAULT_N_VALUE,
        Rp: Optional[float] = DEFAULT_RP,
        As: Optional[float] = DEFAULT_AS,
):
    wc1 = (fp1 + fst1) / 2
    b = signal.firwin(N, wc1, window=win_type, fs=sample_rate)
    return b
