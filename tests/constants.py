from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / 'test_data'
VIDEO_PATH_2160_30FPS = TEST_DATA_DIR / '2160p_30fps.mp4'
VIDEO_PATH_2160_24FPS = TEST_DATA_DIR / '2160p_24fps.mp4'
VIDEO_PATH_2160_60FPS = TEST_DATA_DIR / '2160p_60fps.mkv'
VIDEO_PATH_1080_60FPS = TEST_DATA_DIR / '1080p_60fps.mp4'
VIDEO_PATH_1080_30FPS_VERT = TEST_DATA_DIR / '1080p_30fps_vertical.webm'
VIDEO_PATH_360_60FPS = TEST_DATA_DIR / '360p_60fps.webm'
INVALID_VIDEO_PATH = TEST_DATA_DIR / 'not_a_video.mov'

VIDEO_PATH_2160_30FPS_10MIN = TEST_DATA_DIR / '360p_30fps_10min.mp4'
VID_240P_24FPS = TEST_DATA_DIR / '320x240_24.mp4'
VID_360P_24FPS = TEST_DATA_DIR / '640x360_24.mp4'
VID_720P_24FPS = TEST_DATA_DIR / '1280x720_24.mp4'
VID_1440P_24FPS = TEST_DATA_DIR / '2560x1440_24.mp4'
VID_2160P_30FPS = TEST_DATA_DIR / '3840x2160_30.mp4'
VID_2160P_24FPS = TEST_DATA_DIR / '3840x2160_24.mp4'
VID_1828_X_1332_24FPS = TEST_DATA_DIR / '1828x1332_24.mp4'
VID_1920_X_960 = TEST_DATA_DIR / '1920x960.mp4'

MASTER_PLAYLIST = TEST_DATA_DIR / 'playlists/master.m3u8'
RENDITION_PLAYLIST = TEST_DATA_DIR / 'playlists/rendition.m3u8'
