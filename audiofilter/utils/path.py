from typing import Optional, Tuple

import audiofilter.audio as audio
import numpy as np
import os

MODULE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
ASSETS_DIR = os.path.join(MODULE_DIR, 'assets')
AUDIO_ASSETS_DIR = os.path.join(ASSETS_DIR, 'audio')
EXAMPLE_DIR = os.path.join(AUDIO_ASSETS_DIR, 'example')
DEFAULT_OUTPUT_DIR = os.path.join(AUDIO_ASSETS_DIR, 'output')
DEFAULT_INPUT_DIR = os.path.join(AUDIO_ASSETS_DIR, 'input')
EXAMPLES_LIST = ["Hnoise", "Lnoise", "me", "Mnoise", "nuonuo", "Snoise"]


def validate_path(path: str):
    exist = os.path.exists(path)
    assert exist, f'Path {path} is invalid'


def validate_output_path(path: str):
    exist = os.path.exists(path)
    assert not exist, f'Path {path} is invalid'


def get_local_path(filename: str):
    file_dir = os.path.join(DEFAULT_INPUT_DIR, filename)
    validate_path(file_dir)
    return file_dir


def examples(name: str) -> Tuple[np.ndarray, int]:
    assert name in EXAMPLES_LIST, f'Not found example {name}'
    return audio.validate_load_audio(os.path.join(EXAMPLE_DIR, f'{name}.wav'))


def get_example(name: str) -> str:
    assert name in EXAMPLES_LIST, f'Not found example {name}'
    return os.path.join(EXAMPLE_DIR, f'{name}.wav')