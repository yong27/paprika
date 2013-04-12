import datetime

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect 

from paprika.models import Article, Board
from paprika.views import PaprikaExtraContext


class ArticleList(ListView, PaprikaExtraContext):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.public_in_board(board)


class ArticleCreate(CreateView, PaprikaExtraContext):
    model = Article


class ArticlePublish(RedirectView):
    permanent = False

    def post(self, request, *args, **kwargs):
        article_slug = request.POST.get('slug')
        do_publish = request.POST.get('publish')
        article = get_object_or_404(Article,
            slug=article_slug, board__slug=kwargs['board_slug'])
        if do_publish == 'true':
            article.public_datetime = datetime.datetime.now()
        else:
            article.public_datetime = None
        article.save()
        return HttpResponseRedirect(reverse('article_detail',
            args=(article.id, article.slug)))



class ArticleDetail(DetailView, PaprikaExtraContext):
    model = Article
    context_object_name = 'article'


