import os

from utils.const import PruneConfig


def ensure_directory_exist(directory_path):
    os.makedirs(directory_path, exist_ok=True)


def is_logically_empty(dirs, files):
    real_files = [f for f in files if f not in PruneConfig.FILE_NAMES]
    real_dirs = [d for d in dirs if d not in PruneConfig.DIR_NAMES]

    return not real_files and not real_dirs
