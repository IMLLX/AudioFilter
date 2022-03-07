import os

MODULE_DIR = os.path.join(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(MODULE_DIR, 'assets')
AUDIO_ASSETS_DIR = os.path.join(ASSETS_DIR, 'audio')


def validate_path(path: str):
    exist = os.path.exists(path)
    assert exist, f'Path {path} is invalid'


def get_local_path(filename: str):
    file_dir = os.path.join(AUDIO_ASSETS_DIR, filename)
    validate_path(file_dir)
    return file_dir
