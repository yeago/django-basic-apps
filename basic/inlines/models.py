from django.db import models
from django.contrib.contenttypes.models import ContentType


class InlineType(models.Model):
    """InlineType model"""
    title = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'inline_types'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
