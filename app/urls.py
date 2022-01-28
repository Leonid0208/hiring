from unicodedata import name
from django.urls import path, include
from app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main, name='main'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('desk/', include('desk.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form1.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done1.html"), 
        name="password_reset_complete"),
]
