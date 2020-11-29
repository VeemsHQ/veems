from ffprobe import FFProbe

from .. import transcoder_profiles


def _get_metadata(video_path):
    metadata = FFProbe(str(video_path))
    first_stream = metadata.video[0]
    return {
        'width': int(first_stream.width),
        'height': int(first_stream.height),
    }


def transcode(*, transcode_job, source_file_path):
    """

    TODOs

    1. open the video file with ffmpeg
    2. extract the first video stream.
    3. get the width and height of the video
    4. (not always) if the video is vertical, rotate it.
    5. run the transcode with ffmpeg
    6. upload the resulting webm file to s3 bucket/others
    7. update the transcode job status = COMPLETE
    """
    pass
