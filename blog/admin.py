from django.contrib import admin
from .models import Blog, Blogger, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('title', 'content')
    inlines = [CommentInline]

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'post_date')
    list_filter = ('post_date', 'author')
    search_fields = ('text', 'blog__title')
