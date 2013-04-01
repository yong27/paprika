from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings

from paprika.models import Article, Board, Category, Tag


class HomeView(RedirectView):
    def get_redirect_url(self):
        board = get_object_or_404(Board, slug=settings.HOME_BOARD_SLUG)
        latest_article = Article.objects.public_in_board(board).latest()
        return reverse('article_detail', args=(latest_article.id, latest_article.slug))


class BoardView(RedirectView):
    def get_redirect_url(self, board_slug):
        board = get_object_or_404(Board, slug=board_slug)
        latest_article = Article.objects.public_in_board(board).latest()
        return reverse('article_detail', args=(latest_article.id, latest_article.slug))


class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.public_in_board(self.board)

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context


class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['board'] = context['article'].board
        context['fb_comment_app_id'] = settings.FB_COMMENT_APP_ID
        context['disqus_shortname'] = settings.DISQUS_SHORTNAME
        context['http_host'] = self.request.META['HTTP_HOST']
        return context


class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Category.objects.filter(article__board=self.board)

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context


class CategoryDetail(DetailView):
    model = Category
    context_object_name = 'category'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return super(CategoryDetail, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['board'] = self.board
        context['articles'] = Article.objects.filter(category=context['category'], 
                board=self.board)
        return context


class TagList(ListView):
    model = Tag
    context_object_name = 'tags'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Tag.objects.filter(article__board=self.board).distinct()

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context


class TagDetail(DetailView):
    model = Tag
    context_object_name = 'tag'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return super(TagDetail, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        context['board'] = self.board
        context['articles'] = Article.objects.filter(tags=context['tag'], 
                board=self.board)
        return context
