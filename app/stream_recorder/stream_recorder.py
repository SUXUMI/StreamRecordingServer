import subprocess
from typing import List
import psutil
import time

from .stream_command import StreamCommand


class StreamRecorder:
    """
    Videos/Images Cycle Recording from Stream

    @version 5.0

    5.0, 2021-01-10 - new: code refactoring
    """

    stream: StreamCommand

    error_message = ""

    # how many seconds after restart the stream recording
    # if previous recording process has not been completed
    restart_timeout = 3.

    def __init__(self, stream: StreamCommand) -> None:
        self.stream = stream

    def start(self):
        print(f"Stream recording service started for {self.stream.type.value} \n", end='')

        while True:
            self.__startSingleStreamRecording()
            time.sleep(self.stream.interval)

    def __startSingleStreamRecording(self):
        command = self.stream.get_command()

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # give a some time while process runs subprocess!
        time.sleep(0.5)

        pid = process.pid

        # print(
        #     "START RECORDING: ", self.stream.type.value,
        #     "PID:", pid,
        #     "CHILDREN:",
        #     self.__getProcessChildren(pid),
        # )

        # calculate execution time
        start_time = time.time()
        seconds_elapsed = 0

        while self.__getProcessChildren(pid):
            current_time = time.time()
            seconds_elapsed = current_time - start_time

            # print('seconds_elapsed: ', int(seconds_elapsed) + 1, end="\r", flush=True)

            if seconds_elapsed > self.stream.duration + self.restart_timeout:
                self.error_message = f"max time executed, killing pid: {pid} for {self.stream.type.value}"
                print(f"ERROR: \n{self.error_message}")
                # self.log_error(self.error_message)

                # kill current & child processes
                # psutil.Process(pid).kill()
                self.__killProcess(pid)

                # break
                return False

            time.sleep(1)

        pass

    def __getProcessChildren(self, pid: str) -> List:
        try:
            return psutil.Process(pid).children(recursive=True)
        except:
            return None

    def __killProcess(self, pid: str) -> None:
        try:
            process = psutil.Process(pid)

            for child_proc in process.children(recursive=True):
                child_proc.kill()

            process.kill()
        except:
            return None
