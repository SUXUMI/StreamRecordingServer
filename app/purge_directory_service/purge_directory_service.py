import os, time, sys

from .libs import *


class PurgeDirectoryService:
    dir: str

    # max directory size in Bytes
    max_size: float

    def __init__(self, dir: str, max_size: float) -> None:
        """
        dir - directory full path
        max_size - max allowed size in Gigabytes
        """

        self.dir = dir
        self.max_size = max_size * 1024 * 1024 * 1024

    def start(self) -> None:
        try:
            print("Purge service started\n", end='')

            delete_oldest_file(self.dir)

            while (True):
                if (get_directory_size(self.dir) > self.max_size):
                    delete_oldest_file(self.dir)
                else:
                    # print(time.strftime('%H-%M-%S', time.localtime()), end="\r", flush=True)
                    time.sleep(2)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            time.sleep(10)