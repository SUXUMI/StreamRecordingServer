# Stream Recording Server

Video stream recording dockerized server using python/ffmpeg.

## Usage


### Configuration

Prepare `.env` file, check `.env.example` for the sample.<br>
All possible variables explained below.

```dotenv
# informational
CAM_NAME="Camera 1"

# path where to store the stream recordings
CAM_RECORDINGS_PATH=/data/recordings

# Max capacity size of recording folder in Gigabytes
# for the loop recording, oldest files will be deleted automatically
CAM_RECORDINGS_MAX_SIZE=1

# Video stream uri
CAM_VIDEO_STREAM=rtsp://admin:123456@192.168.0.109:554/live/ch0

# Each video file length in seconds
CAM_VIDEO_RECORDING_DURATION=10

# Video file fps
CAM_VIDEO_RECORDING_FPS=30


# Image stream uri
CAM_IMAGE_STREAM=rtsp://admin:123456@192.168.0.109:554/live/ch0

# Image stream interval for the each next shot
CAM_IMAGE_INTERVAL=10

# Image quality
# Possible values from 1 to 31
# 1 - High, 31 - Low
CAM_IMAGE_QUALITY=15
```

To avoid old files deletion (no loop recording), set `CAM_RECORDINGS_MAX_SIZE` to zero `0`<br>
To record videos from stream, provide `CAM_VIDEO_*` variable details.<br>
To record images from stream, provide `CAM_IMAGE_*` variable details.

### How to run

Docker must be installed first!

Run:

```shell
$ docker-compose up
```

Run in detached mode:

```shell
$ docker-compose up -d
```

After successfull start you should see smth like this:<br>

<pre>
server  | Stream recording service started for video
server  | Stream recording service started for image
server  | Purge service started
</pre>

## Use prebuilt image
Check the docker source: [https://hub.docker.com/repository/docker/suxumi/stream-recording-server](https://hub.docker.com/repository/docker/suxumi/stream-recording-server)