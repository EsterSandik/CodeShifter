import os
import re
import shutil

from utils.config import AppConfig
from utils.const import LoggerMessage
from utils.helpers import is_logically_empty
from utils.logger import logger


def build_file_moves(folder_map):
    file_moves = {}
    for root, _, files in os.walk(AppConfig.BASE_DIR):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), AppConfig.BASE_DIR)
            for key, new_folder in folder_map.items():
                if rel_path.startswith(key) or rel_path == key:
                    new_path = os.path.join(AppConfig.BASE_DIR, new_folder, file)
                    file_moves[os.path.join(AppConfig.BASE_DIR, rel_path)] = new_path
    logger.info(LoggerMessage.Info.MOVE_FILES.format(count=len(file_moves)))
    return file_moves


def ensure_dirs(path, dry_run):
    dir_path = os.path.dirname(path)
    if dry_run:
        logger.info(
            LoggerMessage.DRY_RUN_PREFIX
            + LoggerMessage.Info.CREATE_FOLDER.format(dir_path=dir_path)
        )
    else:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(LoggerMessage.Info.CREATE_FOLDER.format(dir_path=dir_path))
    init_file = os.path.join(dir_path, "__init__.py")
    if not os.path.exists(init_file):
        if dry_run:
            logger.info(
                LoggerMessage.DRY_RUN_PREFIX
                + LoggerMessage.Info.CREATE_INIT.format(init_file=init_file)
            )
        else:
            open(init_file, "a", encoding="utf-8").close()
            logger.info(LoggerMessage.Info.CREATE_INIT.format(init_file=init_file))


def move_files(file_moves, dry_run):
    for old_path, new_path in file_moves.items():
        ensure_dirs(new_path, dry_run)
        if os.path.exists(old_path):
            if dry_run:
                logger.info(
                    LoggerMessage.DRY_RUN_PREFIX
                    + LoggerMessage.Info.MOVE_FILE.format(
                        old_path=old_path, new_path=new_path
                    )
                )
            else:
                shutil.move(old_path, new_path)
                logger.info(
                    LoggerMessage.Info.MOVE_FILE.format(
                        old_path=old_path, new_path=new_path
                    )
                )
        else:
            logger.error(LoggerMessage.Error.NOT_FOUND)


def update_imports(file_moves, dry_run):
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = content
                for old_path, new_path in file_moves.items():
                    old_import = (
                        old_path.replace("src/", "")
                        .replace("/", ".")
                        .replace(".py", "")
                    )
                    new_import = (
                        new_path.replace("src/", "")
                        .replace("/", ".")
                        .replace(".py", "")
                    )
                    new_content = re.sub(rf"\b{old_import}\b", new_import, new_content)

                if new_content != content:
                    if dry_run:
                        logger.info(
                            LoggerMessage.DRY_RUN_PREFIX
                            + LoggerMessage.Info.UPDATE_IMPORTS.format(
                                file_path=file_path
                            )
                        )
                    else:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        logger.info(
                            LoggerMessage.Info.UPDATE_IMPORTS.format(
                                file_path=file_path
                            )
                        )


def find_logically_empty_dirs(base_path, file_moves=None):
    empty_dirs = []
    for root, dirs, files in os.walk(base_path, topdown=False):
        if root == base_path:
            continue

        logical_files = []
        for f in files:
            abs_path = os.path.join(root, f)
            if file_moves and abs_path in file_moves:
                continue
            logical_files.append(f)

        if is_logically_empty(dirs, logical_files):
            empty_dirs.append(root)

    return empty_dirs


def remove_empty_dirs(base_path, dry_run=False, file_moves=None):
    if dry_run:
        for dir in find_logically_empty_dirs(base_path, file_moves):
            logger.info(
                LoggerMessage.DRY_RUN_PREFIX
                + LoggerMessage.Info.REMOVE_DIR.format(dir=dir)
            )
    else:
        removed_any = True
        while removed_any:
            removed_any = False
            for dir in find_logically_empty_dirs(base_path, file_moves):
                shutil.rmtree(dir)
                logger.info(LoggerMessage.Info.REMOVE_DIR.format(dir=dir))
                removed_any = True
