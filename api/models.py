from django.db import models
from django.db.models import SET_NULL, ManyToManyField
from django_extensions.db.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(unique=True, max_length=100)
    content = models.TextField(unique=True)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    tags = ManyToManyField(Tag)

    def __str__(self):
        return self.title
