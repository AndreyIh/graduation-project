from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'content', 'author', 'create_time', 'status' )
    list_editable = ['content', 'status']
    list_filter = ('status', 'create_time', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'create_time'
    ordering = ('status', 'create_time')

admin.site.register(Blog, BlogAdmin)
