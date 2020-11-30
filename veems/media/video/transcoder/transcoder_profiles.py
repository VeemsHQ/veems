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


class WebM720pHigh(WebM720p):
    name = 'webm_720p_high'
    average_rate = 1800
    min_rate = 900
    max_rate = 1800


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


class WebM1080pHigh(WebM1080p):
    name = 'webm_1080p_high'
    average_rate = 3000
    min_rate = 1500
    max_rate = 4350


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


class WebM2160pHigh(WebM2160p):
    name = 'webm_2160p_high'
    average_rate = 18000
    min_rate = 9000
    max_rate = 26100


# TODO: Low/High FPS profiles
# TODO: split audio into m4a for higher quality files?

PROFILES = (
    WebM360p, WebM720p, WebM1080p, WebM1080pHigh, WebM2160p, WebM2160pHigh
)
