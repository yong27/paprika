from django.conf.urls import patterns, url

from paprika.views import HomeView, BoardView
from paprika.views.category import (CategoryList,
        CategoryCreate, CategoryDetail,)
from paprika.views.article import (ArticleList, ArticlePublish,
        ArticleCreate, ArticleDetail, ArticleUpdate)
from paprika.views.tag import TagList, TagDetail
from paprika.feeds import ArticleFeed, ArticleByCategoryFeed

urlpatterns = patterns('',
    url(r'^$',
        HomeView.as_view(), name='home'),
    url(r'^(?P<board_slug>[-\w]+)/$', 
        BoardView.as_view(), name='board'),
    url(r'^(?P<board_slug>[-\w]+)/rss/$', 
        ArticleFeed(), name='article_rss'),
    url(r'^(?P<board_slug>[-\w]+)/category/(?P<slug>[-\w]+)/rss/$', 
        ArticleByCategoryFeed(), name='article_category_rss'),

) + patterns('paprika.views.article',
    url(r'^(?P<board_slug>[-\w]+)/archive/$', 
        ArticleList.as_view(), name='article_list'),
    url(r'^(?P<board_slug>[-\w]+)/archive/create/$', 
        ArticleCreate.as_view(), name='article_create'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/$', 
        ArticleDetail.as_view(), name='article_detail'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/publish/$', 
        ArticlePublish.as_view(), name='article_publish'),
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/update/$', 
        ArticleUpdate.as_view(), name='article_update'),


) + patterns('paprika.views.category',
    url(r'^(?P<board_slug>[-\w]+)/category/$', 
        CategoryList.as_view(), name='category_list'),
    url(r'^(?P<board_slug>[-\w]+)/category/create/$', 
        CategoryCreate.as_view(), name='category_create'),
    url(r'^(?P<board_slug>[-\w]+)/category/(?P<slug>[-\w]+)/$', 
        CategoryDetail.as_view(), name='category_detail'),

) + patterns('paprika.views.tag',
    url(r'^(?P<board_slug>[-\w]+)/tag/$', 
        TagList.as_view(), name='tag_list'),
    url(r'^(?P<board_slug>[-\w]+)/tag/(?P<slug>[-\w]+)/$', 
        TagDetail.as_view(), name='tag_detail'),
)
