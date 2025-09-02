import os

from datetime import time

from dotenv import load_dotenv


load_dotenv()


class AppConfig:
    BASE_DIR = "src"
    DRY_RUN = True


class LogsParams:
    AT_TIME = time(7, 0)
    BACKUPCOUNT = 7
    ENCODING = "utf-8"
    FILE_NAME = "chat_logs.log"
    FORMAT = (
        'time="%(asctime)s" level="%(levelname)s" '
        'source="%(module)s.%(funcName)s:%(lineno)d" '
        'thread=%(thread)d message="%(message)s"'
    )
    INTERVAL = 1
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    WHEN = "midnight"


class Paths:
    LOGS_PATH = os.getenv("LOGS_PATH")


class Route:
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
