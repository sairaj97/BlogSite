from django.urls import path
from .views import *
app_name = 'users'
urlpatterns = [
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('index/', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signup1/', signup1, name='signup1'),
    path('myblog/', MyBlogListView.as_view(), name='myblog'),
    path('blogs/', blog_View.as_view(), name='adminblog'),
    path('edit/<pk>/', blog_edit, name='blog_edit'),
    path('delete/<pk>/', blog_delete, name='blog_delete')
]