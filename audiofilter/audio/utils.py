import os.path
from typing import Union, Tuple, Optional
from audiofilter.utils import (
    DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR
)

import soundfile as sf
import audiofilter.utils as utils
import numpy as np
import librosa


def validate_load_audio(
        audio: Union[str, np.ndarray],
        sample_rate: int = utils.DEFAULT_SAMPLE_RATE
) -> Tuple[np.ndarray, int]:
    if isinstance(audio, str):
        local_path = utils.path.get_local_path(audio)
        return librosa.load(local_path, sr=None, mono=False)
    assert isinstance(audio, np.ndarray), 'Expect type np.ndarray for variable "audio"'

    assert (
            isinstance(sample_rate, int) and sample_rate > 0
    ), "Expected 'sample_rate' to be a positive integer"

    return audio, sample_rate


def save_audio(
        audio: Union[str, np.ndarray],
        filename: str,
        sample_rate: int = utils.DEFAULT_SAMPLE_RATE,
        output_path: Optional[str] = DEFAULT_INPUT_DIR,
) -> Tuple[np.ndarray, int]:
    save_path = os.path.join(output_path, filename)
    utils.validate_output_path(save_path)

    try:
        # Note: librosa reads in audio data as (num_channels, num_samples),
        # but soundfile expects it to be (num_samples, num_channels) when
        # writing it out, so we have to swap axes here.
        saved_audio = np.swapaxes(audio, 0, 1) if audio.ndim > 1 else audio
        sf.write(output_path, saved_audio, sample_rate)
    except Exception as e:
        pass

    return audio, sample_rate
