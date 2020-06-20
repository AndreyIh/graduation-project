from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from blogs.models import Blog


class LatestPostsFeed(Feed):
    title = 'Мой блог'
    link = ''
    description = 'Новый статьи в моем блоге'

    def items(self):
        return Blog.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)