from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

from paprika.models import Article, Board, Tag
from paprika.views import PaprikaExtraContext


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
