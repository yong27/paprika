from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from paprika.models import Article, Board, Category, Tag

class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.filter(board=self.board)

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
