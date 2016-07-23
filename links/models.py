from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class PageData(models.Model):
    page_url = models.CharField(max_length=100, unique=True)
    page_links = ArrayField(models.CharField(max_length=100), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
