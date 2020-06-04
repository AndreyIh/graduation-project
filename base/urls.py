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
from django.contrib import admin
from django.urls import path, include
from routes.views import (travel, find_routes, add_route,
                          RouteListView, RouteDetailView, RouteDeleteView)

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
]
