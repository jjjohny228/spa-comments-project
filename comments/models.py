from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from comments.validators import validate_username, validate_file_type, validate_file_size
from config import settings


def release_upload_to(instance: 'Comment', filename: str) -> str:
    """
    Generates a unique file path for uploaded files.
    The file will be saved to MEDIA_ROOT/comments/author/uuid_string+filename.
    """

    ext = filename.split('.')[-1]
    file_prefix = str(uuid4()).split('-')[0]
    filename = f'{file_prefix}.{ext}'
    return f'comments/{instance.author}/{filename}'


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.CharField(_('User name'), max_length=255, help_text=_('This value may contain only letters, numbers'), validators=[validate_username,])
    email = models.EmailField(_('Email address'))
    home_page = models.URLField(_('Home page'), blank=True, null=True)
    text = models.TextField(_('Your comment'))
    file = models.FileField(_('Attach file'), upload_to=release_upload_to, help_text=_('It should be an image or text file.'), blank=True, null=True, validators=[validate_file_type, validate_file_size,])
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['-created_at']

    def __str__(self):
        return self.text
