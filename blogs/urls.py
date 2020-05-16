from django.urls import path
from .views import (blog_create, BlogUpdateView,
                    BlogDeleteView, SearchResultsView, post_share)

urlpatterns = [
    # path('full/<int:pk>/', BlogDetailView.as_view(), name='full'),
    #path('full/<int:year>/<int:month>/<int:day>/<slug:post>/', BlogDetailView.as_view(), name='full_slug'),
    path('update/<str:slug>/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<str:slug>/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('<int:pk>/share/', post_share, name='post_share'),
    path('add/', blog_create, name='add'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
