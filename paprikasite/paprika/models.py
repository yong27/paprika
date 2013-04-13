from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime

from django.utils.timezone import utc
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy 
from django.core.urlresolvers import reverse
from django.conf import settings


@python_2_unicode_compatible
class Board(models.Model):
    BOARD_TYPE_CHOICES = (
        ('blog', 'Blog'),
        ('web-board', 'Web-board'),
    )
    MARKUP_CHOICES = (
        ('markdown', 'Markdown'),
        ('textile', 'Textile'),
        ('restructuredtext', 'reStructured Text'),
        ('tinymce', 'TinyMCE'),
    )
    type = models.CharField(verbose_name=ugettext_lazy('Board type'),
        help_text=ugettext_lazy('Board type, web-board view supply title only list, '
                    'blog is content included view.'),
        choices=BOARD_TYPE_CHOICES,
        max_length=50, 
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
    markup = models.CharField(verbose_name=ugettext_lazy('Markup language'),
        help_text=ugettext_lazy("Select markup language for this board's article editing"),
        choices=MARKUP_CHOICES,
        max_length=50,
    )

    class Meta:
        verbose_name = ugettext_lazy('Board')
        verbose_name_plural = ugettext_lazy('Boards')
        ordering = ('title',)

    def __str__(self):
        return "[{0}] {1}".format(self.slug, self.title)

    def get_absolute_url(self):
        return reverse('board', args=(self.slug,))


@python_2_unicode_compatible
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
    
    def __str__(self):
        return "[{0}] {1}".format(self.slug, self.title)

    def get_published_article_count(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        return self.article_set.filter(
            public_datetime__lte=now).count()


class ArticleManager(models.Manager):
    def public_in_board(self, board):
        now = datetime.utcnow().replace(tzinfo=utc)
        return Article.objects.filter(
            public_datetime__lte=now, board=board)


@python_2_unicode_compatible
class Article(models.Model):
    board = models.ForeignKey(Board,
        verbose_name=ugettext_lazy('Board'),
        help_text=ugettext_lazy(
            'Board, this article is included in this board.'),
    )
    category = models.ForeignKey(Category,
        verbose_name=ugettext_lazy('Category'), 
        help_text=ugettext_lazy(
            'Category, main classification of this article.'),
        null=True, 
        blank=True,
    )
    title = models.CharField(verbose_name=ugettext_lazy('Title'),
        help_text=ugettext_lazy(
            'Article title, space is permitted.'),
        max_length=200,
    )
    slug = models.CharField(verbose_name=ugettext_lazy('Slug'),
        help_text=ugettext_lazy(
            'Article slug, space is not permitted.'),
        max_length=100,
        unique=True,
    )
    content = models.TextField(
        verbose_name=ugettext_lazy('Content'),
        help_text=ugettext_lazy(
            'Article content, this is saved in HTML format.'),
    )
    created_datetime = models.DateTimeField(
        verbose_name=ugettext_lazy('Created datetime'), 
        help_text=ugettext_lazy('Article created datatime, \
            it is created automatically.'),
        auto_now_add=True,
    )
    modified_datetime = models.DateTimeField(
        verbose_name=ugettext_lazy('Modified datetime'), 
        help_text=ugettext_lazy('Article modified datatime, \
            it is modified automatically.'),
        auto_now=True,
    )
    public_datetime = models.DateTimeField(
        verbose_name=ugettext_lazy('Public datatime'), 
        help_text=ugettext_lazy('Article publication datatime, \
            you can point the time. After this time, this \
            article is open to the public.'),
        null=True, blank=True,
    )
    registrator = models.ForeignKey(User,
        verbose_name=ugettext_lazy('Registrator'),
        help_text=ugettext_lazy('Article registrator'),
    )
    tags = models.ManyToManyField('Tag',
        verbose_name=ugettext_lazy('Tag'),
        help_text=ugettext_lazy(
            'Article tags, multiple tags are permitted'),
        null=True, blank=True,
    )

    objects = ArticleManager()

    class Meta:
        verbose_name = ugettext_lazy('Article')
        verbose_name_plural = ugettext_lazy('Articles')
        ordering = ('-public_datetime', '-created_datetime',)
        get_latest_by = "public_datetime"

    def __str__(self):
        return "Article:{0}".format(self.slug)

    def get_absolute_url(self):
        return reverse('article_detail', args=(self.id, self.slug))

    def get_previous(self):
        ids = [a.id for a in Article.objects.public_in_board(self.board)]
        try:
            order = ids.index(self.id)
            if not order == 0:
                return Article.objects.get(id=ids[order-1])
        except:
            return False

    def get_next(self):
        ids = [a.id for a in Article.objects.public_in_board(self.board)]
        try:
            order = ids.index(self.id)
            if not order == len(ids) - 1:
                return Article.objects.get(id=ids[order+1])
        except ValueError:
            return False


@python_2_unicode_compatible
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

    def __str__(self):
        return "Tag:{0}".format(self.slug)

    def count_articles(self):
        return Article.objects.filter(tags=self).count() 

