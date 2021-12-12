from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', main, name='main'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('desk/', include('desk.urls'))

]
