import datetime

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

from paprika.models import Article, Board
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
    class Meta:
        model = Article
        exclude = ('board', 'public_datetime', 'registrator',)

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)

        title = self.fields.get('title')
        title.widget.attrs['class'] = 'span11'
        slug = self.fields.get('slug')
        slug.widget.attrs['class'] = 'span6'
        content = self.fields.get('content')
        content.widget.attrs['class'] = 'span11'
        content.widget.attrs['rows'] = '15'
        tags = self.fields.get('tags')
        tags.widget=forms.TextInput(
                attrs={'class':'span11'})

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if type(field.widget) in [
                    forms.TextInput,
                    forms.PasswordInput,
                    forms.Textarea]:
                field.widget.attrs['placeholder'] = field.help_text
            field.help_text = '*' if field.required else ''


class ArticleCreate(CreateView, PaprikaExtraContext):
    form_class = ArticleForm
    model = Article

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleCreate, self).dispatch(
                request, *args, **kwargs)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.board = get_object_or_404(
                Board, slug=self.kwargs['board_slug'])
        article.registrator = self.request.user
        article.save()
        return super(ArticleCreate, self).form_valid(form)


class ArticleUpdate(UpdateView, PaprikaExtraContext):
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

