from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog_origin', 'comment_text', 'create_time', 'author', 'lvl', 'comment_origin')
    list_filter = ('create_time', 'blog_origin', 'author',)
    list_editable = ['comment_text', 'lvl', 'comment_origin']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
