"""
Video transcode profiles.

According to recommended specs:
https://developers.google.com/media/vp9/settings/vod
"""

MAX_FRAMERATE = 99999999999


class BaseProfile:
    required_aspect_ratio = None
    format = 'video/webm'


class Webm144p(BaseProfile):
    name = 'webm_144p'
    width = 256
    height = 144
    min_rate = 45
    average_rate = 100
    max_rate = 140
    constant_rate_factor = 40
    tile_columns = 0
    threads = 2
    storage_filename = '144.webm'
    min_framerate = 0
    max_framerate = MAX_FRAMERATE


class Webm240p(BaseProfile):
    name = 'webm_240p'
    width = 320
    height = 240
    average_rate = 150
    min_rate = 75
    max_rate = 218
    constant_rate_factor = 37
    tile_columns = 0
    threads = 2
    storage_filename = '240.webm'
    min_framerate = 0
    max_framerate = MAX_FRAMERATE


class Webm360p(BaseProfile):
    name = 'webm_360p'
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


class Webm360pHigh(Webm360p):
    name = 'webm_360p_high'
    # TODO: adjust bitrate values
    average_rate = 1800
    min_rate = 900
    max_rate = 1800
    min_framerate = 50
    max_framerate = MAX_FRAMERATE


class Webm720p(BaseProfile):
    name = 'webm_720p'
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


class Webm720pHigh(Webm720p):
    name = 'webm_720p_high'
    average_rate = 1800
    min_rate = 900
    max_rate = 1800
    min_framerate = 50
    max_framerate = MAX_FRAMERATE


class Webm1080p(BaseProfile):
    name = 'webm_1080p'
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


class Webm1080pHigh(Webm1080p):
    name = 'webm_1080p_high'
    average_rate = 3000
    min_rate = 1500
    max_rate = 4350
    min_framerate = 50
    max_framerate = MAX_FRAMERATE


class Webm1440p(BaseProfile):
    name = 'webm_1440p'
    width = 2560
    height = 1440
    average_rate = 6000
    min_rate = 3000
    max_rate = 8700
    constant_rate_factor = 24
    tile_columns = 3
    threads = 8
    storage_filename = '1440.webm'
    min_framerate = 0
    max_framerate = 49
    required_aspect_ratio = '16:9'


class Webm1440pHigh(Webm1440p):
    name = 'webm_1440p_high'
    average_rate = 9000
    min_rate = 4500
    max_rate = 13050
    min_framerate = 50
    max_framerate = MAX_FRAMERATE


class Webm2160p(BaseProfile):
    name = 'webm_2160p'
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


class Webm2160pHigh(Webm2160p):
    name = 'webm_2160p_high'
    average_rate = 18000
    min_rate = 9000
    max_rate = 26100
    min_framerate = 50
    max_framerate = MAX_FRAMERATE


# TODO: split audio into m4a for higher quality files?
# TODO: test aspect ratio 2:3 and
# https://en.wikipedia.org/wiki/List_of_common_resolutions

PROFILES = (
    Webm144p, Webm240p, Webm360p, Webm360pHigh, Webm720p, Webm720pHigh,
    Webm1080p, Webm1080pHigh, Webm1440p, Webm1440pHigh, Webm2160p,
    Webm2160pHigh
)


def get_profile(name):
    return [p for p in PROFILES if p.name == name][0]
