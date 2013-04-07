from django.views.generic.base import RedirectView, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.safestring import mark_safe

from paprika.models import Article, Board, Category, Tag


class HomeView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        board = get_object_or_404(Board, slug=settings.HOME_BOARD_SLUG)
        latest_article = Article.objects.public_in_board(board).latest()
        return reverse('article_detail', args=(latest_article.id, latest_article.slug))


class BoardView(RedirectView):
    permanent = False

    def get_redirect_url(self, board_slug):
        board = get_object_or_404(Board, slug=board_slug)
        latest_article = Article.objects.public_in_board(board).latest()
        return reverse('article_detail', args=(latest_article.id, latest_article.slug))


class PaprikaExtraContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(PaprikaExtraContext, self).get_context_data(**kwargs)
        context.update({
            'fb_comment_app_id': settings.FB_COMMENT_APP_ID,
            'disqus_shortname': settings.DISQUS_SHORTNAME,
            'extra_head_html': mark_safe(settings.EXTRA_HEAD_HTML),
            'http_host': self.request.META['HTTP_HOST'],
        })
        if 'board_slug' in self.kwargs:
            context['board'] = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        elif 'article' in context:
            context['board'] = context['article'].board
        return context


class ArticleList(ListView, PaprikaExtraContext):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.public_in_board(board)


class ArticleDetail(DetailView, PaprikaExtraContext):
    model = Article
    context_object_name = 'article'


class CategoryList(ListView, PaprikaExtraContext):
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Category.objects.filter(article__board=board).distinct()


class CategoryDetail(DetailView, PaprikaExtraContext):
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(category=context['category'], 
                board=context['board'])
        return context


class TagList(ListView, PaprikaExtraContext):
    model = Tag
    context_object_name = 'tags'

    def get_queryset(self):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Tag.objects.filter(article__board=board).distinct()


class TagDetail(DetailView, PaprikaExtraContext):
    model = Tag
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(tags=context['tag'], 
                board=context['board'])
        return context
