from django.db import models
from django.db.models import SET_NULL, ManyToManyField




class TimeStampModel(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(TimeStampModel):
    title = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.title


class Category(TimeStampModel):
    title = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.title


class Post(TimeStampModel):
    title = models.CharField(unique=True, max_length=100)
    content = models.TextField(unique=True)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)
    tags = ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.title