from django.conf.urls import patterns, url
from paprika.views import (ArticleList, ArticleDetail, CategoryList, CategoryDetail,
        TagList, TagDetail, HomeView, BoardView)
from paprika.feeds import ArticleFeed

urlpatterns = patterns('',
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'^(?P<board_slug>[-\w]+)/$', 
        BoardView.as_view(), name='board'),
    url(r'^(?P<board_slug>[-\w]+)/rss/$', 
        ArticleFeed(), name='article_rss'),
    url(r'^(?P<board_slug>[-\w]+)/archive/$', 
        ArticleList.as_view(), name='article_list'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', 
        ArticleDetail.as_view(), name='article_detail'),

    url(r'^(?P<board_slug>[-\w]+)/category/$', 
        CategoryList.as_view(), name='category_list'),
    url(r'^(?P<board_slug>[-\w]+)/category/(?P<slug>[-\w]+)/$', 
        CategoryDetail.as_view(), name='category_detail'),

    url(r'^(?P<board_slug>[-\w]+)/tag/$', 
        TagList.as_view(), name='tag_list'),
    url(r'^(?P<board_slug>[-\w]+)/tag/(?P<slug>[-\w]+)/$', 
        TagDetail.as_view(), name='tag_detail'),

)
