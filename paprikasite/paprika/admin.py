from django.contrib import admin
from paprika.models import Board, Category, Article, Tag

class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'slug', 'title', 'type', 'description', 
    )
    list_filter = ('type',)
admin.site.register(Board, BoardAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'slug', 'title'
    )
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_datetime'
    list_display = (
        'board', 'category', 'title', 'slug', 
        'created_datetime', 'modified_datetime', 'public_datetime',
    )
    list_filter = ('board',)
admin.site.register(Article, ArticleAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)
