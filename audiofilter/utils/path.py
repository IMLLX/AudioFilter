from typing import Optional

import os

MODULE_DIR = os.path.join(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(MODULE_DIR, 'assets')
AUDIO_ASSETS_DIR = os.path.join(ASSETS_DIR, 'audio')
EXAMPLE_DIR = os.path.join(AUDIO_ASSETS_DIR, 'example')
DEFAULT_OUTPUT_DIR = os.path.join(AUDIO_ASSETS_DIR, 'output')
DEFAULT_INPUT_DIR = os.path.join(AUDIO_ASSETS_DIR, 'input')


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
