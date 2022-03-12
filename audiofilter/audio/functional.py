from typing import Any, Union, Optional, Tuple
from audiofilter.utils import (DEFAULT_SAMPLE_RATE, DEFAULT_SNR_LEVEL_DB)
from .utils import (validate_load_audio)
from .noise import (gaussian_noise)

import numpy as np
import librosa.effects

AVAILABLE_NOISE_METHOD = ['vectorized', 'maxen', 'axial']


def add_background_noise(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        snr_level_db: Optional[Union[float, int]] = DEFAULT_SNR_LEVEL_DB,
        method: Optional[str] = 'vectorized',
        background_noise: Optional[Union[str, np.ndarray]] = 'gaussian',
) -> Tuple[np.ndarray, int]:
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    assert isinstance(snr_level_db, (int, float)), "Expected 'snr_level_db' to be a number"
    assert method in AVAILABLE_NOISE_METHOD, f"Invalid method {method} "
    if method == 'vectorized':
        Ps = np.sum(audio ** 2 / audio.size)
    elif method == 'maxen':
        Ps = np.max(np.sum(audio ** 2 / audio.shape[0], axis=0))
    else:
        Ps = np.sum(audio ** 2 / audio.shape[0], axis=0)

    Psdb = 10 * np.log10(Ps)
    Pn = Psdb - snr_level_db
    if background_noise and isinstance(background_noise, str):
        assert background_noise in ['gaussian'], f"Invalid noise {background_noise}"
        if background_noise == 'gaussian':
            audio, sample_rate = gaussian_noise(audio, Pn, sample_rate)
        # TODO band_gaussian_noise
    else:
        assert audio.shape == background_noise.shape
        audio = audio + background_noise

    return audio, sample_rate


def speed(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        factor: float = 2.,
) -> Tuple[np.ndarray, int]:
    assert isinstance(factor, (int, float)) and factor > 0, "Expected 'factor' to be a positive number"
    audio, sample_rate = validate_load_audio(audio, sample_rate)

    audio = librosa.effects.time_stretch(audio, rate=factor)
    return audio, sample_rate
