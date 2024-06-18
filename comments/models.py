import imghdr

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.conf import settings


# manage creation of the folder for each Release object
def release_upload_to(instance: 'Comment', filename: str) -> str:
    """
    Generates a unique file path for uploaded files.
    The file will be saved to MEDIA_ROOT/comments/author/uuid_string+filename.
    """

    ext = filename.split('.')[-1]
    file_prefix = str(uuid4()).split('-')[4]
    filename = f'{file_prefix}.{ext}'
    return f'comments/{instance.author}/{filename}'


def get_file_extension(file):
    return file.name.split('.')[-1].lower()


def validate_file_size(value):
    """
    Function to validate uploaded file size

    """
    file_extension = get_file_extension(value)
    # Check if file is text type
    if file_extension in settings.ALLOWED_IMAGE_FILE_EXTENSIONS:
        return
    max_size = 100 * 1024  # 100 KB
    if value.size > max_size:
        raise ValidationError(_('File size must be less than 100KB.'))


def validate_file_type(value):
    """
    Function to validate uploaded file type

    """
    file_type = get_file_extension(value)
    if file_type not in settings.ALLOWED_IMAGE_FILE_EXTENSIONS and settings.ALLOWED_TEXT_FILE_EXTENSIONS:
        raise ValidationError(_('Invalid file type.'))


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.CharField(_('User name'), max_length=255)
    email = models.EmailField(_('Email address'))
    home_page = models.URLField(_('Home page'), blank=True, null=True)
    text = models.TextField(_('Your comment'))
    file = models.FileField(_('Attach some file'), upload_to=release_upload_to, blank=True, null=True, validators=[validate_file_type, validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-created_at']

    def __str__(self):
        return self.text[:20]
