import pytest

from veems.media.transcoder import transcoder_profiles
from veems.media import thumbnails
from veems.media import models

pytestmark = pytest.mark.django_db


def test_get_autogenerated_thumbnail_choices(
    video,
    rendition_thumbnails_factory,
):
    # Create 3 Video Renditions with 3 Thumbnails each.
    num_thumbs_per_rendition = 3
    for profile_cls in (
        transcoder_profiles.Webm360p,
        transcoder_profiles.Webm720p,
        transcoder_profiles.Webm1080p,
    ):
        rendition_thumbnails_factory(
            video=video,
            width=profile_cls.width,
            height=profile_cls.height,
            num_thumbnails=num_thumbs_per_rendition,
        )

    thumbnail_records = thumbnails.get_autogenerated_thumbnail_choices(
        video_record=video
    )

    assert len(thumbnail_records) == num_thumbs_per_rendition
    assert [t.time_offset_secs for t in thumbnail_records] == [1, 11, 21]
    for thumbnail in thumbnail_records:
        assert isinstance(thumbnail, models.VideoRenditionThumbnail)
        assert thumbnail.height == transcoder_profiles.Webm720p.height
