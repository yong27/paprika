from django.views.generic.base import RedirectView, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe

from paprika.models import Article, Board


class HomeView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        board = get_object_or_404(Board, slug=settings.HOME_BOARD_SLUG)
        try:
            latest_article = Article.objects.public_in_board(
                    board).latest()
            return reverse('article_detail',
                    args=(latest_article.id, latest_article.slug))
        except ObjectDoesNotExist:
            return reverse('article_list', args=(board.slug,))


class BoardView(RedirectView):
    permanent = False

    def get_redirect_url(self, board_slug):
        board = get_object_or_404(Board, slug=board_slug)
        try:
            latest_article = Article.objects.public_in_board(board).latest()
            return reverse('article_detail', args=(latest_article.id, latest_article.slug))
        except ObjectDoesNotExist:
            return reverse('article_list', args=(board.slug,))


class PaprikaExtraContext(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(PaprikaExtraContext, self).get_context_data(**kwargs)
        context.update({
            'fb_comment_app_id': settings.FB_COMMENT_APP_ID,
            'disqus_shortname': settings.DISQUS_SHORTNAME,
            'extra_head_html': mark_safe(settings.EXTRA_HEAD_HTML),
            'http_host': self.request.META['HTTP_HOST'],
            'user_paprika_comment': settings.USE_PAPRIKA_COMMENT,
            'user': self.request.user,
        })
        if 'board_slug' in self.kwargs:
            context['board'] = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        elif 'article' in context:
            context['board'] = context['article'].board
        return context
