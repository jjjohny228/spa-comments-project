from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.text[:20]
