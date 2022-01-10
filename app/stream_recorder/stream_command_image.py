import os
import datetime

from .output_type import OutputType
from .stream_command import StreamCommand
from .log_level import LogLevel


class StreamCommandImage(StreamCommand):
    type = OutputType.IMAGE

    duration = 1

    interval: int

    # image quality = 7    [1 - 31, 1 - High, 31 - Lowest]
    quality: int

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'recordings')

    extension = 'jpg'

    def __init__(
        self,
        stream_uri: str,
        dir: str = None,
        name: str = "Camera 1",
        interval: int = 30,
        quality: int = 7,
        options: str = "",
        loglevel: LogLevel = LogLevel.ERROR,
    ) -> None:
        """
        stream_uri - required
        dir - full path where to store recordings
        name - actually, the subfolder name for video recordings
        interval - interval between shots
        quality - image quality, [1 - High, 31 - Lowest]
        options - additional options
        loglevel - possible values: quiet, panic, fatal, error, warning, info, debug
        """

        self.stream_uri = stream_uri

        if dir != None:
            self.dir = dir

        self.name = os.path.basename(self.dir) if name == None else name

        self.interval = interval
        self.quality = quality
        self.options = options
        self.loglevel = loglevel.value

    def get_command(self):
        now = datetime.datetime.now()

        folder = '{}{}{}'.format(now.year, str(now.month).zfill(2), str(now.day).zfill(2))
        filename = '{}-{}{}{}.{}'.format(folder, str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2), self.extension)

        # directory path where to store recordings
        path_dir = os.path.join(self.dir, folder)

        # full path of media file where to store
        path_full = os.path.join(path_dir, filename)

        # if directory not exists, create it recursively
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        
        self.options += ' -frames:v 1 -q:v ' + str(self.quality)

        cmd = f'ffmpeg -y -rtsp_transport tcp -i "{self.stream_uri}" -loglevel {self.loglevel} {self.options} "{path_full}"'

        return cmd
    
    pass
