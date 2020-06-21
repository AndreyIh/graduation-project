"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from routes.views import (travel, find_routes, add_route,
                          RouteListView, RouteDetailView, RouteDeleteView)
from django.contrib.sitemaps.views import sitemap

from .feeds import LatestPostsFeed
from .sitemaps import BlogSitemap

sitemaps = {'blogs': BlogSitemap, }

from blogs.views import home
from .views import resume

urlpatterns = [
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('admin/', admin.site.urls),
    path('author/<str:author>/', home, name='author'),
    path('resume/', resume, name='resume'),
    path('comments/', include(('comments.urls', 'comments'))),
    path('cities/', include(('cities.urls', 'cities'))),
    path('trains/', include(('trains.urls', 'trains'))),
    path('blog/', include(('blogs.urls', 'blog'))),
    path('travel/', travel, name='travel'),
    path('find/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('list/', RouteListView.as_view(), name='list'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
    path('dialogs/', include(('private_chat.urls', 'dialogs'))),
    path('', home, name='home'),
    path('tag/<slug:tag_slug>/', home, name='post_list_by_tag'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)