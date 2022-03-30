from typing import Optional, Union, Any
from .content import (
    DEFAULT_GSTOP, DEFAULT_GPASS, DEFAULT_N_VALUE, DEFAULT_RS, DEFAULT_RP
)
import numpy as np
import scipy.signal as signal
import audiofilter.display as display

pi = np.pi
tan = np.tan


def IIR_filter_design(
        sample_rate: Union[int, float],
        band_type: str,
        irr_type: str,
        fp1: float,
        fst1: float,
        gs: Optional[float] = DEFAULT_GSTOP,
        gp: Optional[float] = DEFAULT_GPASS,
        Rp: Optional[float] = DEFAULT_RP,
        Rs: Optional[float] = DEFAULT_RS,
        ax=None,
        ax1=None,
        ax2=None,
        cla: bool = False
):
    Fs = sample_rate
    T = 1 / Fs
    wp = 2 * pi * fp1 / Fs
    ws = 2 * pi * fst1 / Fs
    omega_p = (2 / T) * tan(wp / 2)
    omega_s = (2 / T) * tan(ws / 2)
    if irr_type == 'butter':
        N, Wn = signal.buttord(omega_p, omega_s, gp, gs, True)
        b, a = signal.butter(N, Wn, band_type, analog=True)
    elif irr_type == 'chebyI':
        N, Wn = signal.cheb1ord(omega_p, omega_s, gp, gs, True)
        b, a = signal.cheby1(N, Rp, Wn, band_type, analog=True)  # rp
    elif irr_type == 'chebyII':
        N, Wn = signal.cheb2ord(omega_p, omega_s, gp, gs, True)
        b, a = signal.cheby2(N, Rs, Wn, band_type, analog=True)  # rs
    else:
        N, Wn = signal.ellipord(omega_p, omega_s, gp, gs, True)
        b, a = signal.ellip(N, Rp, Rs, Wn, band_type, analog=True)  # rp,rs
    if N > 30:
        raise Exception("Too Large N the filter might be meaningless")
    b_dig, a_dig = signal.bilinear(b, a, fs=Fs)
    w, h = signal.freqz(b_dig, a_dig)

    if ax:
        if cla:
            ax.cla()
        ax.semilogx(w / (2 * pi) * Fs, 20 * np.log10(abs(h)))
        ax.set_title('filter frequency response')
        ax.set_xlabel('Frequency [Hz / second]')
        ax.set_ylabel('Amplitude [dB]')
        ax.margins(0, 0.1)
        ax.grid(which='both', axis='both')
    if ax1:
        if cla:
            ax1.cla()
        display.display_zero_pole(b_dig, a_dig, ax1)

    if ax2:
        if cla:
            ax2.cla()
        display.display_angle_plot(w / (2 * pi) * Fs, h, ax2)

    return b_dig, a_dig


def IIR_band_filter_design(
        sample_rate: Union[int, float],
        band_type: str,
        irr_type: str,
        fp1: float,
        fst1: float,
        fp2: Optional[float] = None,
        fst2: Optional[float] = None,
        gs: Optional[float] = DEFAULT_GSTOP,
        gp: Optional[float] = DEFAULT_GPASS,
        Rp: Optional[float] = DEFAULT_RP,
        Rs: Optional[float] = DEFAULT_RS,
        ax=None,
        ax1=None,
        ax2=None,
        cla: bool = False
):
    Fs = sample_rate
    T = 1 / Fs
    wp1 = 2 * pi * fp1 / Fs
    ws1 = 2 * pi * fst1 / Fs
    wp2 = 2 * pi * fp2 / Fs
    ws2 = 2 * pi * fst2 / Fs
    omega_p1 = (2 / T) * tan(wp1 / 2)
    omega_s1 = (2 / T) * tan(ws1 / 2)
    omega_p2 = (2 / T) * tan(wp2 / 2)
    omega_s2 = (2 / T) * tan(ws2 / 2)
    # print(omega_p1, omega_s1, omega_p2, omega_s2)
    if irr_type == 'butter':
        N, Wn = signal.buttord([omega_p1, omega_p2], [omega_s1, omega_s2], gp, gs, True)
        b, a = signal.butter(N, Wn, band_type, analog=True)
    elif irr_type == 'chebyI':
        N, Wn = signal.cheb1ord([omega_p1, omega_p2], [omega_s1, omega_s2], gp, gs, True)
        b, a = signal.cheby1(N, Rp, Wn, band_type, analog=True)
    elif irr_type == 'chebyII':
        N, Wn = signal.cheb2ord([omega_p1, omega_p2], [omega_s1, omega_s2], gp, gs, True)
        b, a = signal.cheby2(N, Rs, Wn, band_type, analog=True)
    else:
        N, Wn = signal.ellipord([omega_p1, omega_p2], [omega_s1, omega_s2], gp, gs, True)
        b, a = signal.ellip(N, Rp, Rs, Wn, band_type, analog=True)
    if N > 30:
        raise Exception("Too Large N the filter might be meaningless")
    b_dig, a_dig = signal.bilinear(b, a, fs=Fs)

    w, h = signal.freqz(b_dig, a_dig)

    if ax:
        if cla:
            ax.cla()
        ax.semilogx(w / (2 * pi) * Fs, 20 * np.log10(abs(h)))
        ax.set_title('filter frequency response')
        ax.set_xlabel('Frequency [Hz / second]')
        ax.set_ylabel('Amplitude [dB]')
        ax.margins(0, 0.1)
        ax.grid(which='both', axis='both')

    if ax1:
        if cla:
            ax1.cla()
        display.display_zero_pole(b_dig, a_dig, ax1)

    if ax2:
        if cla:
            ax2.cla()
        display.display_angle_plot(w / (2 * pi) * Fs, h, ax2)

    return b_dig, a_dig


def FIR_filter_design(
        sample_rate: Union[int, float],
        band_type: str,
        win_type: str,
        fp1: float,
        fst1: float,
        N: int = DEFAULT_N_VALUE,
        Rp: Optional[float] = DEFAULT_RP,
        Rs: Optional[float] = DEFAULT_RS,
        ax=None,
        ax1=None,
        ax2=None,
        cla: bool = False
):
    wc1 = (fp1 + fst1) / 2
    b = signal.firwin(N, wc1, window=win_type, fs=sample_rate, pass_zero=band_type)
    w, h = signal.freqz(b, 1)

    if ax:
        if cla:
            ax.cla()
        ax.semilogx(w / (2 * pi) * sample_rate, 20 * np.log10(abs(h)))
        ax.set_title('filter frequency response')
        ax.set_xlabel('Frequency [Hz / second]')
        ax.set_ylabel('Amplitude [dB]')
        ax.margins(0, 0.1)
        ax.grid(which='both', axis='both')

    if ax1:
        if cla:
            ax1.cla()
        display.display_zero_pole(b, 1, ax1)

    if ax2:
        if cla:
            ax2.cla()
        display.display_angle_plot(w / (2 * pi) * sample_rate, h, ax2)

    return b


def FIR_band_filter_design(
        sample_rate: Union[int, float],
        band_type: str,
        win_type: str,
        fp1: float,
        fst1: float,
        fp2: Optional[float] = None,
        fst2: Optional[float] = None,
        N: int = DEFAULT_N_VALUE,
        ax=None,
        ax1=None,
        ax2=None,
        cla: bool = False
):
    wc1 = (fp1 + fst1) / 2
    wc2 = (fp2 + fst2) / 2
    b = signal.firwin(N, [wc1, wc2], window=win_type, fs=sample_rate, pass_zero=band_type)
    w, h = signal.freqz(b, 1)

    if ax:
        if cla:
            ax.cla()
        ax.semilogx(w / (2 * pi) * sample_rate, 20 * np.log10(abs(h)))
        ax.set_title('filter frequency response')
        ax.set_xlabel('Frequency [Hz / second]')
        ax.set_ylabel('Amplitude [dB]')
        ax.margins(0, 0.1)
        ax.grid(which='both', axis='both')

    if ax1:
        if cla:
            ax1.cla()
        display.display_zero_pole(b, 1, ax1)

    if ax2:
        if cla:
            ax2.cla()
        display.display_angle_plot(w / (2 * pi) * sample_rate, h, ax2)

    return b
