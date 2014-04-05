from django.views.generic.base import TemplateView
from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404

from paprika.models import Article, Board
from paprika.views import PaprikaExtraContext


class SearchForm(forms.Form):
    q = forms.CharField()

    def search(self, board):
        text = self.cleaned_data['q']
        queryset = Article.objects.public_in_board(board).filter(
                Q(content__icontains=text) | Q(title__icontains=text))
        return queryset


class SearchView(TemplateView, PaprikaExtraContext):
    template_name = 'paprika/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            context['articles'] = form.search(board)
        return context

