from .models import Users, User_details, Post
from .forms import RegistrationForm1, RegistrationForm2, LogInForm, PostForm
from . import views
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib import messages
from django.urls import reverse
from django.views.generic.list import ListView

# Create your views here.

def signup1(request):
    # check if the request is post
    if request.method == 'POST':
        #current_user = request.user
        # Pass the form data to the form class
        details = RegistrationForm1(request.POST)

        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            #post.user_id = current_user.id
            # Finally write the changes into database
            post.save()

            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponse("Register successfully")

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "signup.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = RegistrationForm1(None)
        return render(request, 'signup.html', {'form': form})


def signup(request):
    # check if the request is post
    if request.method == 'POST':

        # Pass the form data to the form class
        details = RegistrationForm2(request.POST)

        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            # Finally write the changes into database
            post.save()

            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect(reverse('users:signup1'))

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "signup.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = RegistrationForm2(None)
        return render(request, 'signup.html', {'form': form})


def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect(reverse('users:index'))
        #return render(request, 'index.html')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponse("Login successfully")
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'login.html', {'form': form, 'error': error})


def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))


def index(request):
    error = False
    if request.method == "POST":
        current_user = request.user
        #ob = Users.objects.filter(id = current_user.id).first()
        #obj = Post(user = current_user.id)
        #obj = Post.objects.filter(user = current_user.id).first()
        details = PostForm(request.POST)
        if details.is_valid():
            post = details.save(commit=False)
            post.user_id = current_user.id
            post.posted_by = current_user
            post.save()
            return redirect(reverse('users:index'))
                #render(request, 'index.html', {'form': details, 'error': error})
    else:
        form = PostForm()
        return render(request, 'index.html', {'form': form, 'error': error})

    return redirect(reverse('users:index'))


class MyBlogListView(ListView):
    model = Post
    template_name = 'my_blog.html'
    context_object_name = "myblog"
    ordering = "-time_stamp"

    def get_queryset(self):
        return Post.objects.filter(user_id=self.request.user.id)



"""
class Admin_View(ListView):
    model = Post
    template_name = 'admin_blog.html'
    context_object_name = "adminblog"
    ordering = "-time_stamp"

    def get_queryset1(self):
        return Post.objects.filter(user_id=self.request.user.id)

"""
class blog_View(ListView):
    model = Post
    template_name = 'admin_blog.html'
    context_object_name = "adminblog"
    ordering = "-time_stamp"

    def get_queryset(self):
        if 1==self.request.user.is_admin:
            return Post.objects.all()
        else:
            return Post.objects.filter(user_id=self.request.user.id)


def blog_edit(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        post = PostForm(request.POST or None, instance=obj)
        if post.is_valid():
            post.save()
            return redirect(reverse('users:myblog'))
    else:
        form = PostForm(instance=obj)
        return render(request, "edit.html", {'form': form})

def blog_delete(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        details = PostForm(request.POST or None, instance=obj)
        if details.is_valid():
            post = details.save(commit=False)
            post.is_deleted = True
            post.save()
            return redirect(reverse('users:myblog'))
    else:
        form = PostForm(instance=obj)
        return render(request, "delete.html", {'form': form})