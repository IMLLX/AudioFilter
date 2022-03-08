from typing import Union, Optional
from audiofilter.utils import (
    DEFAULT_SAMPLE_RATE,
)
from audiofilter.audio.utils import validate_load_audio

import simpleaudio as sa
import numpy as np


def play_sound(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> sa.PlayObject:
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    n_channels = audio.ndim
    audio = audio * (2 ** 15 - 1) / np.max(np.abs(audio))
    audio_int16 = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio_int16, n_channels, 2, sample_rate)
    play_obj.wait_done()
    return play_obj
