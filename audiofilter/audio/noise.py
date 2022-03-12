from typing import Union, Tuple, Optional
from audiofilter.utils import (
    DEFAULT_SAMPLE_RATE, DEFAULT_SNR_LEVEL_DB
)
from audiofilter.audio.utils import validate_load_audio

import numpy as np


def gaussian_noise(
        audio: Union[np.ndarray, str],
        Pn: Union[float, int],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> Tuple[np.ndarray, int]:
    # audio, sample_rate = validate_load_audio(audio, sample_rate)
    noise = np.sqrt(10 ** (Pn / 10)) * np.random.normal(0, 1, audio.shape)
    return audio + noise, sample_rate

