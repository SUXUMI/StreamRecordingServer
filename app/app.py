import os, concurrent.futures

from stream_recorder.stream_command_video import StreamCommandVideo
from stream_recorder.stream_command_image import StreamCommandImage
from stream_recorder.stream_recorder import StreamRecorder
from purge_directory_service.purge_directory_service import PurgeDirectoryService


try:
    NAME = os.environ["CAM_NAME"]

    RECORDINGS_PATH = os.environ["CAM_RECORDINGS_PATH"]
    RECORDINGS_MAX_SIZE = float(os.environ["CAM_RECORDINGS_MAX_SIZE"])

    VIDEO_STREAM = os.environ["CAM_VIDEO_STREAM"]
    VIDEO_RECORDING_DURATION = int(os.environ["CAM_VIDEO_RECORDING_DURATION"])
    VIDEO_RECORDING_FPS = float(os.environ["CAM_VIDEO_RECORDING_FPS"])

    IMAGE_STREAM = os.environ["CAM_IMAGE_STREAM"]
    IMAGE_INTERVAL = int(os.environ["CAM_IMAGE_INTERVAL"])
    IMAGE_QUALITY = int(os.environ["CAM_IMAGE_QUALITY"])

    video_stream_command: StreamCommandVideo = None
    image_stream_command: StreamCommandImage = None

    if len(VIDEO_STREAM):
        video_stream_command = StreamCommandVideo(
            stream_uri=VIDEO_STREAM,
            dir=RECORDINGS_PATH,
            name=NAME,
            duration=VIDEO_RECORDING_DURATION,
            fps=VIDEO_RECORDING_FPS,
        )

    if len(IMAGE_STREAM):
        image_stream_command = StreamCommandImage(
            stream_uri=IMAGE_STREAM,
            dir=RECORDINGS_PATH,
            name=NAME,
            interval=IMAGE_INTERVAL,
            quality=IMAGE_QUALITY,
        )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # start video stream recording
        if video_stream_command:
            executor.submit(StreamRecorder(video_stream_command).start)

        # start image stream recording
        if image_stream_command:
            executor.submit(StreamRecorder(image_stream_command).start)

        executor.submit(PurgeDirectoryService(dir = RECORDINGS_PATH, max_size = RECORDINGS_MAX_SIZE).start)
    pass
except Exception as e:
    print("INIT ERROR:", str(e))
