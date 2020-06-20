from django.contrib.sitemaps import Sitemap
from blogs.models import Blog


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.updated