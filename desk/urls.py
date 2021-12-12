from django.urls import path, include
from desk.views import *


urlpatterns = [
    path('', main, name='desk'),
    path('dialogs/', DialogsView.as_view(), name='dialogs'),
    path('dialogs/create/<int:user_id>/', CreateDialogView.as_view(), name='create_dialog'),
    path('dialogs/<int:chat_id>', MessagesView.as_view(), name='messages'),
    path('create/resume/', CreateResume.as_view(), name='create_resume')
]

# url(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
# url(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),