from typing import Union, Tuple, Optional

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
        sample_rate: int = utils.DEFAULT_SAMPLE_RATE,
        output_path: Optional[str] = None,
) -> Tuple[np.ndarray, int]:
    pass
