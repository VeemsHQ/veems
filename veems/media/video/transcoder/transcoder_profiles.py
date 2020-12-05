"""
Video transcode profiles.

According to recommended specs:
https://developers.google.com/media/vp9/settings/vod
"""


class WebM360p:
    name = 'webm_360p'
    format = 'video/webm'
    width = 640
    height = 360
    average_rate = 276
    min_rate = 138
    max_rate = 400
    constant_rate_factor = 36
    tile_columns = 1
    threads = 4
    storage_filename = '360.webm'
    min_framerate = 0
    max_framerate = 49


class WebM360pHigh(WebM360p):
    name = 'webm_360p_high'
    # TODO: adjust bitrate values
    average_rate = 1800
    min_rate = 900
    max_rate = 1800
    min_framerate = 50
    max_framerate = 99999999999


class WebM720p:
    name = 'webm_720p'
    format = 'video/webm'
    width = 1280
    height = 720
    average_rate = 1024
    min_rate = 512
    max_rate = 1485
    constant_rate_factor = 32
    tile_columns = 2
    threads = 7
    storage_filename = '720.webm'
    min_framerate = 0
    max_framerate = 49


class WebM720pHigh(WebM720p):
    name = 'webm_720p_high'
    average_rate = 1800
    min_rate = 900
    max_rate = 1800
    min_framerate = 50
    max_framerate = 99999999999


class WebM1080p:
    name = 'webm_1080p'
    format = 'video/webm'
    width = 1920
    height = 1080
    average_rate = 1800
    min_rate = 900
    max_rate = 2610
    constant_rate_factor = 31
    tile_columns = 3
    threads = 8
    storage_filename = '1080.webm'
    min_framerate = 0
    max_framerate = 49


class WebM1080pHigh(WebM1080p):
    name = 'webm_1080p_high'
    average_rate = 3000
    min_rate = 1500
    max_rate = 4350
    min_framerate = 50
    max_framerate = 99999999999


class WebM2160p:
    name = 'webm_2160p'
    format = 'video/webm'
    width = 3840
    height = 2160
    average_rate = 12000
    min_rate = 6000
    max_rate = 17400
    constant_rate_factor = 15
    tile_columns = 3
    threads = 24
    storage_filename = '2160.webm'
    min_framerate = 0
    max_framerate = 49


class WebM2160pHigh(WebM2160p):
    name = 'webm_2160p_high'
    average_rate = 18000
    min_rate = 9000
    max_rate = 26100
    min_framerate = 50
    max_framerate = 99999999999


# TODO: split audio into m4a for higher quality files?

PROFILES = (
    WebM360p, WebM360pHigh, WebM720p, WebM720pHigh, WebM1080p, WebM1080pHigh,
    WebM2160p, WebM2160pHigh
)


def get_profile(name):
    return [p for p in PROFILES if p.name == name][0]
