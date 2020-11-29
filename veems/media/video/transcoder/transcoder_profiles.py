

class WebM360p:
    name = 'webm360p'
    format = 'video/webm'
    width = 640
    height = 360
    bitrate = 500
    audio_bitrate = 80
    storage_filename = '360.webm'

class WebM720p:
    name = 'webm720p'
    format = 'video/webm'
    width = 1280
    height = 720
    bitrate = 1000
    audio_bitrate = 128
    storage_filename = '720.webm'

# TODO: 1080,,,etc 4k

PROFILES = (
    WebM360p,
    WebM720p
)
