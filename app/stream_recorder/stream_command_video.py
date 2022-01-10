import os
import datetime

from .output_type import OutputType
from .stream_command import StreamCommand
from .log_level import LogLevel


class StreamCommandVideo(StreamCommand):
    fps: int

    type = OutputType.VIDEO

    dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'recordings')
    
    # better format, in this case - terminated recording video is readable
    extension = 'avi'

    # extension = 'mp4'

    def __init__(
        self,
        stream_uri: str,
        dir: str = None,
        name: str = "Camera 1",
        duration: int = 300,
        interval: int = 0,
        fps: float = 30,
        options: str = "-vcodec copy",
        loglevel: LogLevel = LogLevel.ERROR,
    ) -> None:
        """
        stream_uri - required
        dir - full path where to store recordings
        name - yet, just informational
        duration - video file recording duration
        interval - interval between shots
        fps - recording fps
        options - additional options
        loglevel - possible values: quiet, panic, fatal, error, warning, info, debug
        """

        self.stream_uri = stream_uri

        if dir != None:
            self.dir = dir

        self.name = os.path.basename(self.dir) if name == None else name

        self.duration = duration
        self.interval = interval
        self.fps = fps
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

        cmd = f'ffmpeg -y -rtsp_transport tcp -i "{self.stream_uri}" -r {self.fps} -loglevel {self.loglevel} {self.options} -t {self.duration} "{path_full}"'

        return cmd
    
    pass
