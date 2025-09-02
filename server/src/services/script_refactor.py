from utils.config import AppConfig
from utils.const import LoggerMessage
from utils.files import build_file_moves, move_files, remove_empty_dirs, update_imports
from utils.logger import logger


def run_refactor(folder_map, dry_run=True):
    try:
        file_moves = build_file_moves(folder_map)
        move_files(file_moves, dry_run)
        update_imports(file_moves, dry_run)
        remove_empty_dirs(AppConfig.BASE_DIR, dry_run, file_moves)
    except Exception as e:
        error_message = LoggerMessage.Error.RUN_REFACTOR.format(error=e)
        logger.error(error_message)
        raise Exception(error_message)
