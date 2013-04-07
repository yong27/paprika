from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from paprika.models import Board, Article, Category
from paprika.templatetags.markups import markdown


class ArticleFeed(Feed):
    def get_object(self, request, board_slug):
        return get_object_or_404(Board, slug=board_slug)

    def title(self, board):
        return board.title

    def link(self, board):
        return board.get_absolute_url()

    def description(self, board):
        return board.description

    def items(self, board):
        return Article.objects.public_in_board(board)[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.content)


class ArticleByCategoryFeed(ArticleFeed):
    def get_object(self, request, board_slug, slug):
        board = super(ArticleByCategoryFeed, self).get_object(request, board_slug)
        self.category = get_object_or_404(Category, slug=slug)
        return board

    def items(self, board):
        return Article.objects.public_in_board(board).filter(category=self.category)[:30]
