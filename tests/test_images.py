from exif import Image as ExifImage

from veems import images


def test_remove_exif_data(uploaded_img_with_exif):
    img_file_obj, _ = uploaded_img_with_exif

    result_file_obj = images.remove_exif_data(img_file_obj)

    # Check all exif data was removed
    exif_image = ExifImage(result_file_obj)
    assert exif_image.list_all() == []
