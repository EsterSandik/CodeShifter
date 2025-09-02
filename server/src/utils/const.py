class LoggerMessage:
    DRY_RUN_PREFIX = "[DRY RUN] "

    class Error:
        RUN_REFACTOR = "Error during run refactor: {error}"
        NOT_FOUND = "File not found: {old_path}"

    class Info:
        CREATE_FOLDER = "Create folder: {dir_path}"
        CREATE_INIT = "Create init: {init_file}"
        MOVE_FILES = "Detected {count} files to move."
        MOVE_FILE = "Move: {old_path} → {new_path}"
        UPDATE_IMPORTS = "Update imports in: {file_path}"
        REMOVE_DIR = "Remove dir: {dir}"


class PruneConfig:
    DIR_NAMES = ["__pycache__"]
    FILE_NAMES = ["__init__.py"]
