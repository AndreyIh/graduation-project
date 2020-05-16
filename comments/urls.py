from django.urls import path, include
from comments.views import add_answer_comment, comment_view


urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', comment_view, name='comment'),
    path('<int:pk_b>/<int:pk_c>', add_answer_comment, name='answer'),
]
