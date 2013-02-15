from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from paprika.models import Article, Board

class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'

class BoardArticleList(ArticleList):
    def get_queryset(self):
        self.board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.filter(board=self.board)

    def get_context_data(self, **kwargs):
        context = super(BoardArticleList, self).get_context_data(**kwargs)
        context['board'] = self.board
        return context

class ArticleDetail(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        context['board'] = context['article'].board
        return context
