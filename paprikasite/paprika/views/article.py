import datetime
import re

from django import forms
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect 
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy 
from django.db import transaction

from paprika.models import Article, Board, Tag
from paprika.views import PaprikaExtraContext


class ArticleList(ListView, PaprikaExtraContext):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        return Article.objects.public_in_board(board)

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['unpublished_articles'] = Article.objects.filter(public_datetime__isnull=True)
        return context


class ArticleForm(forms.ModelForm):
    custom_tags = forms.CharField(
            label=ugettext_lazy('Tags'), required=False,
            help_text = ugettext_lazy(
                'Seperate by comma(",") about each tag'))

    class Meta:
        model = Article
        exclude = ('public_datetime', 'tags')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields['board'].widget = forms.HiddenInput()
        self.fields['registrator'].widget = forms.HiddenInput()
        title = self.fields.get('title')
        title.widget.attrs['class'] = 'span11'
        slug = self.fields.get('slug')
        slug.widget.attrs['class'] = 'span6'
        content = self.fields.get('content')
        content.widget.attrs['class'] = 'span11'
        content.widget.attrs['rows'] = '15'
        custom_tags = self.fields.get('custom_tags')
        custom_tags.widget.attrs['class'] = 'span11'

        if kwargs.get('instance'):
            tags_value = kwargs['instance'].tags.values_list(
                    'slug', flat=True)
            custom_tags.initial = ", ".join(tags_value)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if type(field.widget) in [
                    forms.TextInput,
                    forms.PasswordInput,
                    forms.Textarea]:
                field.widget.attrs['placeholder'] = field.help_text
            field.help_text = '*' if field.required else ''

    @transaction.autocommit
    def save(self, *args, **kwargs):
        article = super(ArticleForm, self).save(*args, **kwargs)
        article.tags = []
        for slug in self.cleaned_data['custom_tags'].split(','):
            if not slug:
                continue
            slug = re.sub('^\s+|\s+$' ,'', slug)
            tag, created = Tag.objects.get_or_create(
                    slug=slug)
            article.tags.add(tag)
        return article


class ArticleCreate(CreateView, PaprikaExtraContext):
    form_class = ArticleForm
    model = Article

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(
                request, *args, **kwargs)

    def get_initial(self):
        context = self.get_context_data()
        initial = {}
        initial['board'] = context['board']
        initial['registrator'] = context['user']
        return initial

    def form_valid(self, form):
        article = form.save()
        article.board = get_object_or_404(
                Board, slug=self.kwargs['board_slug'])
        article.registrator = self.request.user
        article.save()
        return super(ArticleCreate, self).form_valid(form)


class ArticleUpdate(UpdateView, PaprikaExtraContext):
    form_class = ArticleForm
    model = Article


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

