from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _l
from tinymce.models import HTMLField

class Board(models.Model):
    BOARD_TYPE_CHOICES = (
        ('blog', 'blog'),
        ('web-board', 'web-board'),
    )
    type = models.CharField(verbose_name=_l('Board type'),
        help_text=_l('Board type, web-board view supply title only list, '
                    'blog is content included view.'),
        max_length=50, choices=BOARD_TYPE_CHOICES,
    )
    title = models.CharField(verbose_name=_l('Title'),
        help_text=_l('Board title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=_l('Slug'),
        help_text=_l('Board slug, space is not permitted, it is used in URL.'),
        max_length=100,
    )
    description = HTMLField(verbose_name=_l('Description'),
        help_text=_l('Board description, it is displayed in main page.'),
    )

    class Meta:
        verbose_name = _l('Board')
        verbose_name_plural = _l('Boards')
        ordering = ('title',)

    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Category(models.Model):
    title = models.CharField(verbose_name=_l('Title'),
        help_text=_l('Category title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=_l('Slug'),
        help_text=_l('Category slug, space is not permitted, it is used in URL.'),
        max_length=100,
    )

    class Meta:
        verbose_name = _l('Category')
        verbose_name_plural = _l('Categorys')
        ordering = ('title',)
    
    def __unicode__(self):
        return "[{0}] {1}".format(self.slug, self.title)


class Article(models.Model):
    board = models.ForeignKey(Board, verbose_name=_l('Board'),
        help_text=_l('Board, this article is included in this board.'),
    )
    category = models.ForeignKey(Category, verbose_name=_l('Category'), 
        help_text=_l('Category, main classification of this article.'),
        null=True, 
        blank=True,
    )
    title = models.CharField(verbose_name=_l('Title'),
        help_text=_l('Article title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=_l('Slug'),
        help_text=_l('Article slug, space is not permitted.'),
        max_length=100,
    )
    content =HTMLField(verbose_name=_l('Content'),
        help_text=_l('Article content, this is saved in HTML format.'),
    )
    created_datetime = models.DateTimeField(verbose_name=_l('Created datetime'), 
        help_text=_l('Article created datatime, it is created automatically.'),
        auto_now_add=True,
    )
    modified_datetime = models.DateTimeField(verbose_name=_l('Modified datetime'), 
        help_text=_l('Article modified datatime, it is modified automatically.'),
        auto_now=True,
    )
    public_datetime = models.DateTimeField(verbose_name=_l('Public datatime'), 
        help_text=_l('Article publication datatime, you can point the time. '
                     'After this time, this article is open to the public.'),
        null=True, 
        blank=True,
    )
    registrator = models.ForeignKey(User, verbose_name=_l('Registrator'),
        help_text=_l('Article registrator'),
    )
    tags = models.ForeignKey('Tag', verbose_name=_l('Tag'),
        help_text=_l('Article tags, multiple tags are permitted'),
    )

    class Meta:
        verbose_name = _l('Article')
        verbose_name_plural = _l('Articles')
        ordering = ('-created_datetime',)

    def __unicode__(self):
        return "Article:{0}".format(self.slug)


class Tag(models.Model):
    slug = models.CharField(verbose_name=_l('Slug'),
        help_text=_l('Tag slug, space is not permitted.'),
        max_length=100,
    )

    class Meta:
        verbose_name = _l('Tag')
        verbose_name_plural = _l('Tags')
        ordering = ('slug',)

    def __unicode__(self):
        return "Tag:{0}".format(self.slug)
