import logging
from io import BytesIO

from PIL import Image as PilImage, ImageOps
from django.core.files.uploadedfile import SimpleUploadedFile

logger = logging.getLogger(__name__)


def remove_exif_data(image_file):
    logger.info('Removing exif data from image...')
    original = PilImage.open(image_file)
    # rotate image to correct orientation before removing EXIF data
    original = ImageOps.exif_transpose(original)
    # create output image, forgetting the EXIF metadata
    stripped = PilImage.new(original.mode, original.size)
    stripped.putdata(tuple(original.getdata()))

    buffer = BytesIO()
    extension = image_file.name.split('.')[-1].upper()
    extension_to_format = {
        'JPG': 'JPEG',
    }
    format_ = extension_to_format.get(extension, extension)
    stripped.save(buffer, format_)
    return SimpleUploadedFile(image_file.name, buffer.getvalue())
