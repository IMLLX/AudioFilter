from typing import Union, Optional
from audiofilter.utils import (
    DEFAULT_SAMPLE_RATE,
)
from audiofilter.audio.utils import validate_load_audio

import simpleaudio
import simpleaudio as sa
import numpy as np


def play_sound(
        audio: Union[np.ndarray, str],
        sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> simpleaudio.PlayObject:
    audio, sample_rate = validate_load_audio(audio, sample_rate)
    n_channels = audio.shape[-1]
    audio_int16 = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio_int16, n_channels, 2, sample_rate)

    return play_obj
