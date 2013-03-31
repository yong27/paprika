from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from paprika.models import Board, Article


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
