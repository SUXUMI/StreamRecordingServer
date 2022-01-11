import os, concurrent.futures

from stream_recorder.stream_command_video import StreamCommandVideo
from stream_recorder.stream_command_image import StreamCommandImage
from stream_recorder.stream_recorder import StreamRecorder
from purge_directory_service.purge_directory_service import PurgeDirectoryService
try:
    NAME = os.environ["CAM_NAME"] if "CAM_NAME" in os.environ else "Camera"

    RECORDINGS_PATH = (
        os.environ["CAM_RECORDINGS_PATH"]
        if "CAM_RECORDINGS_PATH" in os.environ
        else os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "..", "recordings"
        )
    )
    RECORDINGS_MAX_SIZE = float(os.environ["CAM_RECORDINGS_MAX_SIZE"]) if "CAM_RECORDINGS_MAX_SIZE" in os.environ else 0.

    VIDEO_STREAM = os.environ["CAM_VIDEO_STREAM"] if "CAM_VIDEO_STREAM" in os.environ else ""
    VIDEO_RECORDING_DURATION = int(os.environ["CAM_VIDEO_RECORDING_DURATION"]) if "CAM_VIDEO_RECORDING_DURATION" in os.environ else 300
    VIDEO_RECORDING_FPS = float(os.environ["CAM_VIDEO_RECORDING_FPS"]) if "CAM_VIDEO_RECORDING_FPS" in os.environ else 30

    IMAGE_STREAM = os.environ["CAM_IMAGE_STREAM"] if "CAM_IMAGE_STREAM" in os.environ else ""
    IMAGE_INTERVAL = int(os.environ["CAM_IMAGE_INTERVAL"]) if "CAM_IMAGE_INTERVAL" in os.environ else 30
    IMAGE_QUALITY = int(os.environ["CAM_IMAGE_QUALITY"]) if "CAM_IMAGE_QUALITY" in os.environ else 15

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
    else:
        print("NO VIDEO_STREAM")

    if len(IMAGE_STREAM):
        image_stream_command = StreamCommandImage(
            stream_uri=IMAGE_STREAM,
            dir=RECORDINGS_PATH,
            name=NAME,
            interval=IMAGE_INTERVAL,
            quality=IMAGE_QUALITY,
        )
    else:
        print("NO IMAGE_STREAM")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # start video stream recording
        if video_stream_command:
            executor.submit(StreamRecorder(video_stream_command).start)

        # start image stream recording
        if image_stream_command:
            executor.submit(StreamRecorder(image_stream_command).start)

        # start purge service
        if RECORDINGS_MAX_SIZE:
            executor.submit(
                PurgeDirectoryService(
                    dir=RECORDINGS_PATH, max_size=RECORDINGS_MAX_SIZE
                ).start
            )
    
except Exception as e:
    print("INIT ERROR:", str(e))
