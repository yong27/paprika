from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy 
from tinymce.models import HTMLField

class Board(models.Model):
    BOARD_TYPE_CHOICES = (
        ('blog', 'blog'),
        ('web-board', 'web-board'),
    )
    type = models.CharField(verbose_name=ugettext_lazy('Board type'),
        help_text=ugettext_lazy('Board type, web-board view supply title only list, '
                    'blog is content included view.'),
        max_length=50, choices=BOARD_TYPE_CHOICES,
    )
    title = models.CharField(verbose_name=ugettext_lazy('Title'),
        help_text=ugettext_lazy('Board title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=ugettext_lazy('Slug'),
        help_text=ugettext_lazy('Board slug, space is not permitted, it is used in URL.'),
        max_length=100,
        unique=True,
    )
    description = models.TextField(verbose_name=ugettext_lazy('Description'),
        help_text=ugettext_lazy('Board description, it is displayed in main page.'),
    )

    class Meta:
        verbose_name = ugettext_lazy('Board')
        verbose_name_plural = ugettext_lazy('Boards')
        ordering = ('title',)

    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Category(models.Model):
    title = models.CharField(verbose_name=ugettext_lazy('Title'),
        help_text=ugettext_lazy('Category title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=ugettext_lazy('Slug'),
        help_text=ugettext_lazy('Category slug, space is not permitted, it is used in URL.'),
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = ugettext_lazy('Category')
        verbose_name_plural = ugettext_lazy('Categories')
        ordering = ('title',)
    
    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Article(models.Model):
    board = models.ForeignKey(Board, verbose_name=ugettext_lazy('Board'),
        help_text=ugettext_lazy('Board, this article is included in this board.'),
    )
    category = models.ForeignKey(Category, verbose_name=ugettext_lazy('Category'), 
        help_text=ugettext_lazy('Category, main classification of this article.'),
        null=True, 
        blank=True,
    )
    title = models.CharField(verbose_name=ugettext_lazy('Title'),
        help_text=ugettext_lazy('Article title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=ugettext_lazy('Slug'),
        help_text=ugettext_lazy('Article slug, space is not permitted.'),
        max_length=100,
        unique=True,
    )
    content =HTMLField(verbose_name=ugettext_lazy('Content'),
        help_text=ugettext_lazy('Article content, this is saved in HTML format.'),
    )
    created_datetime = models.DateTimeField(verbose_name=ugettext_lazy('Created datetime'), 
        help_text=ugettext_lazy('Article created datatime, it is created automatically.'),
        auto_now_add=True,
    )
    modified_datetime = models.DateTimeField(verbose_name=ugettext_lazy('Modified datetime'), 
        help_text=ugettext_lazy('Article modified datatime, it is modified automatically.'),
        auto_now=True,
    )
    public_datetime = models.DateTimeField(verbose_name=ugettext_lazy('Public datatime'), 
        help_text=ugettext_lazy('Article publication datatime, you can point the time. '
                     'After this time, this article is open to the public.'),
        null=True, 
        blank=True,
    )
    registrator = models.ForeignKey(User, verbose_name=ugettext_lazy('Registrator'),
        help_text=ugettext_lazy('Article registrator'),
    )
    tags = models.ForeignKey('Tag', verbose_name=ugettext_lazy('Tag'),
        help_text=ugettext_lazy('Article tags, multiple tags are permitted'),
    )

    class Meta:
        verbose_name = ugettext_lazy('Article')
        verbose_name_plural = ugettext_lazy('Articles')
        ordering = ('-created_datetime',)

    def __unicode__(self):
        return "Article:{0}".format(self.slug)


class Tag(models.Model):
    slug = models.CharField(verbose_name=ugettext_lazy('Slug'),
        help_text=ugettext_lazy('Tag slug, space is not permitted.'),
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = ugettext_lazy('Tag')
        verbose_name_plural = ugettext_lazy('Tags')
        ordering = ('slug',)

    def __unicode__(self):
        return "Tag:{0}".format(self.slug)
