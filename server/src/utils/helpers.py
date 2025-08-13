import os


def ensure_directory_exist(directory_path):
    os.makedirs(directory_path, exist_ok=True)
