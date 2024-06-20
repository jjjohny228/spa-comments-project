import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def get_file_extension(file):
    """
    Function helps to get file extension

    """
    return file.name.split('.')[-1].lower()


def validate_file_size(value):
    """
    Function to validate uploaded file size

    """
    file_extension = get_file_extension(value)
    # Check if file is text type
    if file_extension in settings.ALLOWED_TEXT_FILE_EXTENSIONS:
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


def validate_username(value):
    """
    Validate that the username contains only Latin letters and digits.
    """
    if not re.match(r'^[a-zA-Z0-9]+$', value):
        raise ValidationError(
            _('User Name can only contain letters and digits from the Latin alphabet.'),
            params={'value': value},
        )
