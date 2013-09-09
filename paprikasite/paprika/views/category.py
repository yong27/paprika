from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.db.models import Count

from paprika.models import Category, Board, Article
from paprika.views import PaprikaExtraContext


class CategoryList(ListView, PaprikaExtraContext):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        board = get_object_or_404(Board, slug=self.kwargs['board_slug'])
        context['categories'] = Category.objects.filter(article__board=board,
                ).annotate(num_articles=Count('article')
                ).order_by('num_articles')
        return context


class CategoryCreate(CreateView, PaprikaExtraContext):
    model = Category

    @method_decorator(user_passes_test(lambda u: u.is_staff or u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryCreate, self).dispatch( request, *args, **kwargs)

    def get_success_url(self):
        return reverse('category_list', args=[self.kwargs['board_slug']])


class CategoryDetail(DetailView, PaprikaExtraContext):
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.public_in_board(context['board']
                ).filter(category=context['category'])
        return context


