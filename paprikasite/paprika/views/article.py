import datetime

from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect 
from django.utils.decorators import method_decorator

from paprika.models import Article, Board
from paprika.views import PaprikaExtraContext


class ArticleList(ListView, PaprikaExtraContext):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        board = get_object_or_404(Board,
            slug=self.kwargs['board_slug'])
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.public_in_board(board)


class ArticleCreate(CreateView, PaprikaExtraContext):
    model = Article

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(
                request, *args, **kwargs)


class ArticlePublish(RedirectView):
    permanent = False

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlePublish, self).dispatch(
                request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        do_publish = request.POST.get('publish')
        article = get_object_or_404(Article,
            slug=kwargs['slug'], id=kwargs['object_id'])
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

