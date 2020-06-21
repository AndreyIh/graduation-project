from django.urls import path
from .views import (login_view, logout_view, register_view, personal_cabinet,
                    MyPasswordChangeView, MyPasswordChangeDoneView, MyPasswordResetDoneView,
                    MyPasswordResetConfirmView, MyPasswordResetCompleteView, MyPasswordResetView, edit_profile)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('password_change/', MyPasswordChangeView.as_view(),
         name='password_change'),
    path('password_reset/',  MyPasswordResetView.as_view(),
         name='password_reset'),
    path('password_change/done/', MyPasswordChangeDoneView.as_view(),
                              name='password_change_done'),
    path('password_reset/done/', MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('edit/', edit_profile, name='edit')
]
