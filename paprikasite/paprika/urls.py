from django.conf.urls import patterns, url
from paprika.views import BoardArticleList, ArticleDetail

urlpatterns = patterns('',
    url(r'^(?P<board_slug>[-\w]+)/$', 
        BoardArticleList.as_view(), 
        name='article_list'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', 
        ArticleDetail.as_view(), 
        name='article_detail'),
)
