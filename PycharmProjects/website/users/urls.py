from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
urlpatterns = [
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('blogpost/', blogpost, name='blogpost'),
    path('index/', index1, name='index1'),
    path('signup/', signup, name='signup'),
    path('user_signup/', user_signup, name='user_signup'),
    path('signup1/', signup1, name='signup1'),
    path('myblog/', MyBlogListView.as_view(), name='myblog'),
    path('blogs/', blog_View.as_view(), name='adminblog'),
    path('edit/<pk>/', blog_edit, name='blog_edit'),
    path('delete/<pk>/', blog_delete, name='blog_delete'),
    path('adminedit/<pk>/', admin_edit, name='admin_edit'),
    path('admindelete/<pk>/', admin_delete, name='admin_delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)