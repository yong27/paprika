from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Board(models.Model):
    BOARD_TYPE_CHOICES = (
        ('blog', 'blog'),
        ('web-board', 'web-board'),
    )
    type = models.CharField(max_length=50, choices=BOARD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=10)
    description = HTMLField()

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=10)

    class Meta:
        ordering = ('title',)
    
    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Article(models.Model):
    board = models.ForeignKey(Board)
    category = models.ForeignKey(Category, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=100)
    content =HTMLField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    public_datetime = models.DateTimeField(null=True, blank=True)
    registrator = models.ForeignKey(User)
    tags = models.ForeignKey('Tag')

    class Meta:
        ordering = ('-created_datetime',)

    def __unicode__(self):
        return "Article:{0}".format(self.slug)


class Tag(models.Model):
    slug = models.CharField(max_length=100)

    class Meta:
        ordering = ('slug',)

    def __unicode__(self):
        return "Tag:{0}".format(self.slug)
