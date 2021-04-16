import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3

from veems.media import models

pytestmark = pytest.mark.django_db


@pytest.fixture
def video_rendition(video, simple_uploaded_file):
    return models.VideoRendition.objects.create(
        video=video,
        file=simple_uploaded_file,
        name='webm_360p',
        profile='webm_360p',
        ext='webm',
        file_size=1,
    )


def test_transcode_job(transcode_job):
    assert str(transcode_job) == (
        f'<TranscodeJob {transcode_job.id} webm_360p created>'
    )


def test_upload_file_upload_to(upload):
    result = models._upload_file_upload_to(
        instance=upload, filename='blah.mp4'
    )

    assert result == f'uploads/{upload.id}.mp4'


def test_video_rendition_upload_to(video_rendition):
    result = models._video_rendition_upload_to(
        instance=video_rendition, filename='360p.webm'
    )

    assert result == (
        f'videos/{video_rendition.video_id}/renditions'
        f'/{video_rendition.id}/rendition/'
        f'{video_rendition.id}.webm'
    )


from exif import Image as ExifImage


def test_video_custom_thumbnail_image(video_factory, uploaded_img_with_exif):
    img_file_obj, img_path = uploaded_img_with_exif

    with img_path.open('rb') as file_:
        exif_image = ExifImage(file_)
    assert exif_image.has_exif
    assert exif_image.list_all() == [
        'image_description',
        'make',
        'model',
        'orientation',
        'x_resolution',
        'y_resolution',
        'resolution_unit',
        'software',
        'datetime',
        'y_and_c_positioning',
        '_exif_ifd_pointer',
        '_gps_ifd_pointer',
        'compression',
        'jpeg_interchange_format',
        'jpeg_interchange_format_length',
        'exposure_time',
        'f_number',
        'exposure_program',
        'photographic_sensitivity',
        'exif_version',
        'datetime_original',
        'datetime_digitized',
        'components_configuration',
        'exposure_bias_value',
        'max_aperture_value',
        'metering_mode',
        'light_source',
        'flash',
        'focal_length',
        'maker_note',
        'user_comment',
        'flashpix_version',
        'color_space',
        'pixel_x_dimension',
        'pixel_y_dimension',
        '_interoperability_ifd_Pointer',
        'file_source',
        'scene_type',
        'custom_rendered',
        'exposure_mode',
        'white_balance',
        'digital_zoom_ratio',
        'focal_length_in_35mm_film',
        'scene_capture_type',
        'gain_control',
        'contrast',
        'saturation',
        'sharpness',
        'subject_distance_range',
        'gps_latitude_ref',
        'gps_latitude',
        'gps_longitude_ref',
        'gps_longitude',
        'gps_altitude_ref',
        'gps_timestamp',
        'gps_satellites',
        'gps_img_direction_ref',
        'gps_map_datum',
        'gps_datestamp',
    ]

    video = video_factory(custom_thumbnail_image=img_file_obj)

    assert video.custom_thumbnail_image
    # from PIL import Image, ImageOps
    # import PIL
    # img = Image.open(video.custom_thumbnail_image)
    # exif = {
    #     PIL.ExifTags.TAGS[k]: v
    #     for k, v in img._getexif().items()
    #     if k in PIL.ExifTags.TAGS
    # }
    # import ipdb; ipdb.set_trace()
    exif_image = ExifImage(video.custom_thumbnail_image)
    import ipdb; ipdb.set_trace()
    exif = exif_image.list_all()
    assert exif == [
        'image_description',
        'make',
        'model',
        'orientation',
        'x_resolution',
        'y_resolution',
        'resolution_unit',
        'software',
        'datetime',
        'y_and_c_positioning',
        '_exif_ifd_pointer',
        '_gps_ifd_pointer',
        'compression',
        'jpeg_interchange_format',
        'jpeg_interchange_format_length',
        'exposure_time',
        'f_number',
        'exposure_program',
        'photographic_sensitivity',
        'exif_version',
        'datetime_original',
        'datetime_digitized',
        'components_configuration',
        'exposure_bias_value',
        'max_aperture_value',
        'metering_mode',
        'light_source',
        'flash',
        'focal_length',
        'maker_note',
        'user_comment',
        'flashpix_version',
        'color_space',
        'pixel_x_dimension',
        'pixel_y_dimension',
        '_interoperability_ifd_Pointer',
        'file_source',
        'scene_type',
        'custom_rendered',
        'exposure_mode',
        'white_balance',
        'digital_zoom_ratio',
        'focal_length_in_35mm_film',
        'scene_capture_type',
        'gain_control',
        'contrast',
        'saturation',
        'sharpness',
        'subject_distance_range',
        'gps_latitude_ref',
        'gps_latitude',
        'gps_longitude_ref',
        'gps_longitude',
        'gps_altitude_ref',
        'gps_timestamp',
        'gps_satellites',
        'gps_img_direction_ref',
        'gps_map_datum',
        'gps_datestamp',
    ]


def test_video_rendition_thumbnail_upload_to(
    video_rendition, simple_uploaded_img_file
):
    video_rendition_thumbnail = models.VideoRenditionThumbnail.objects.create(
        video_rendition=video_rendition,
        time_offset_secs=1,
        height=10,
        width=10,
        ext='.jpg',
        file=simple_uploaded_img_file,
    )

    result = models._video_rendition_thumbnail_upload_to(
        instance=video_rendition_thumbnail, filename='something.jpg'
    )

    assert result == (
        f'videos/{video_rendition_thumbnail.video_rendition.video_id}/'
        f'renditions/{video_rendition_thumbnail.video_rendition.id}/'
        f'thumbnails/{video_rendition_thumbnail.id}.jpg'
    )


class TestUpload:
    def test_set_file_using_uploaded_file(self, channel):
        upload = models.Upload.objects.create(
            presigned_upload_urls=[
                'https://objectstorage/?part_num=1',
                'https://objectstorage/?part_num=2',
                'https://objectstorage/?part_num=3',
            ],
            media_type='video',
            channel=channel,
        )
        file_ = SimpleUploadedFile(
            'video.mp4',
            b'data',
        )

        upload.file = file_
        upload.save()
        upload.refresh_from_db()

        assert upload.file.name == f'uploads/{upload.id}.mp4'
        assert upload.file.url.startswith('http')
        assert 'AccessKeyId' in upload.file.url

    def test_file_uploaded_outside_the_applocation(self, settings, channel):
        # This tests the flow where the file is uploaded to the storage
        # bucket completely outside of the application itself
        # (on the client side using pre-signed-url upload process
        upload = models.Upload.objects.create(
            presigned_upload_urls=[
                'https://objectstorage/?part_num=1',
                'https://objectstorage/?part_num=2',
                'https://objectstorage/?part_num=3',
            ],
            media_type='video',
            channel=channel,
        )

        uploaded_filename = f'{upload.id}/video.mp4'

        # Upload the file completely outside of Django
        s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)
        s3.upload_fileobj(
            io.BytesIO(b'data'),
            models.STORAGE_BACKEND.bucket_name,
            uploaded_filename,
        )

        # Set the Django file field to point to that file path
        upload.file.name = uploaded_filename
        upload.save()

        # Check file can be accessed as if it was uploaded within Django
        upload.refresh_from_db()
        assert upload.file.name == uploaded_filename
        assert upload.file.url.startswith('http')
        assert 'AccessKeyId' in upload.file.url, upload.file.url
        assert upload.id in upload.file.url
