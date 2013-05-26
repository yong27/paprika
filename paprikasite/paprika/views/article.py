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
from django.utils.timezone import utc

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
        context['unpublished_articles'] = Article.objects.filter(
                public_datetime__isnull=True)
        return context


class ArticleForm(forms.ModelForm):
    custom_tags = forms.CharField(label=ugettext_lazy('Tags'), 
            help_text = ugettext_lazy('Seperate by comma(",") about each tag'),
            required=False)

    class Meta:
        model = Article
        fields = ('category', 'title', 'slug', 'content')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'span11'
        self.fields['slug'].widget.attrs['class'] = 'span11'
        self.fields['content'].widget.attrs = {
            'class': 'span11',
            'rows': '18',
        }
        self.fields['custom_tags'].widget.attrs['class'] = 'span11'

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if type(field.widget) in [
                    forms.TextInput,
                    forms.PasswordInput,
                    forms.Textarea]:
                field.widget.attrs['placeholder'] = field.help_text
            field.help_text = '*' if field.required else ''

        instance = kwargs.get('instance')
        if instance:
            tags_value = instance.tags.values_list('slug', flat=True)
            self.fields['custom_tags'].initial = ", ".join(tags_value)
            self.set_board_and_registrator(instance.board, instance.registrator)

    def clean_custom_tags(self):
        custom_tags = self.cleaned_data.get('custom_tags')
        if custom_tags:
            return [t.strip() for t in custom_tags.split(',')]
        else:
            return []

    def set_board_and_registrator(self, board, registrator):
        self.board = board
        self.registrator = registrator

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        article = super(ArticleForm, self).save(*args, **kwargs)
        article.board = self.board
        article.registrator = self.registrator
        article.save()
        for tag in article.tags.all():
            article.tags.remove(tag)
            if not tag.article_set.exists():
                tag.delete()
        for tag_string in self.cleaned_data['custom_tags']:
            tag, created = Tag.objects.get_or_create(slug=tag_string)
            article.tags.add(tag)
        return article


class ArticleCreate(CreateView, PaprikaExtraContext):
    form_class = ArticleForm
    model = Article

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        form.set_board_and_registrator(board, self.request.user)
        return super(ArticleCreate, self).form_valid(form)


class ArticleUpdate(UpdateView, PaprikaExtraContext):
    form_class = ArticleForm
    model = Article


class ArticlePublish(RedirectView):
    permanent = False

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticlePublish, self).dispatch( request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        do_publish = request.POST.get('publish')
        article = get_object_or_404(Article,
            slug=kwargs['slug'], id=kwargs['object_id'])
        if do_publish == 'true':
            article.public_datetime = datetime.datetime.utcnow().replace(
                    tzinfo=utc)
        else:
            article.public_datetime = None
        article.save()
        return HttpResponseRedirect(reverse('article_detail',
            args=(article.id, article.slug)))


class ArticleDetail(DetailView, PaprikaExtraContext):
    model = Article
    context_object_name = 'article'

