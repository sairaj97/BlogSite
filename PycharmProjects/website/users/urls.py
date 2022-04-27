from django.urls import path
from .views import log_in, log_out, index

urlpatterns = [
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('index/', index, name='index')
]