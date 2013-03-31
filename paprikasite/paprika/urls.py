from django.conf.urls import patterns, url
from paprika.views import ArticleList, ArticleDetail, CategoryList, CategoryDetail

urlpatterns = patterns('',
    url(r'^(?P<board_slug>[-\w]+)/$', 
        ArticleList.as_view(), name='article_list'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', 
        ArticleDetail.as_view(), name='article_detail'),

    url(r'^(?P<board_slug>[-\w]+)/category/$', 
        CategoryList.as_view(), name='category_list'),
    url(r'^(?P<board_slug>[-\w]+)/category/(?P<slug>[-\w]+)/$', 
        CategoryDetail.as_view(), name='category_detail'),
)
