from typing import Any, Union, Optional, Tuple

import librosa.effects

from audiofilter.utils import DEFAULT_SAMPLE_RATE

import utils as audutils
import numpy as np

import fitfilt


def add_background_noise(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        snr_level_db: float = 10.0,
        background_noise: Optional[Union[str, np.ndarray]] = None,
        output_path: Optional[str] = None,
) -> Tuple[np.ndarray, int]:
    pass


def speed(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        factor: float = 2.,
) -> Tuple[np.ndarray, int]:
    assert isinstance(factor, (int, float)) and factor > 0, "Expected 'factor' to be a positive number"
    audio, sample_rate = audutils.validate_load_audio(audio, sample_rate)

    audio = librosa.effects.time_stretch(audio, rate=factor)
    return audio, sample_rate
