from .models import Users, User_details, Post
from .forms import RegistrationForm1, RegistrationForm2, LogInForm, PostForm
from . import views
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib import messages
from django.urls import reverse
from django.views.generic.list import ListView
from django.http import JsonResponse
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
            return JsonResponse({'statusCode': 200, 'message': "Details submitted Successfully"})

            # redirect it to some another page indicating data
            # was inserted successfully
            #return redirect(reverse('users:signup'))

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "signup1.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = RegistrationForm1(None)
        return render(request, 'signup1.html', {'form': form})

#
def signup(request):
    # check if the request is post
    if request.user.is_authenticated:
        return redirect(reverse('users:index1'))
    if request.method == 'POST':
        #if request.POST.get('submit') == 'Signup':
            # Pass the form data to the form class
        details  = RegistrationForm2(request.POST)

        if details.is_valid():
            details.save()
            return JsonResponse({'statusCode': 200, 'message': "Inserted Successfully"})
            #return redirect(reverse('users:signup1'))
            #     # Temporarily make an object to be add some
            #     # logic into the data if there is such a need
            #     # before writing to the database
            #     post = details.save(commit=False)
            # # Finally write the changes into database
            #     post.save()

                #return redirect(reverse('users:signup1'))


        elif request.POST.get('submit') == 'Login':
            form = LogInForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                try:
                    user = authenticate(request, email=email, password=password)
                except:
                    return JsonResponse({'statusCode': 401,"message": "Invalid credential"})
                if user is not None:
                    login(request, user)
                    return JsonResponse({'statusCode': 202,"message": "User Login Success"})
                else:
                    return JsonResponse({'statusCode': 401,"message": "Invalid credential"})


                #print(username, password)
                # user = authenticate(email=email, password=password)
                # if user:
                #     login(request, user)
                #     return redirect(reverse('users:index1'))
                # else:
                #     error = True

    else:
        return render(request, 'home1.html')


def user_signup(request):
    user = Users.objects.get(pk=45)
    print(type(user))
    json_user = {}
    json_user['email'] = user.email
    json_user['password'] = user.password
    json_user['username'] = user.username
    print(user)
    print(user.username)
    print(user.email)
    print(user.phone_number)
    exit()
    user = Users()
    user.username = request.POST['username']
    user.email = request.POST['email']
    user.phone_number=request.POST['phone_number']
    user.save()
    return JsonResponse({'statusCode': 200, 'message': "Inserted Successfully"})



def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect(reverse('users:blogpost'))
        #return render(request, 'blogpost.html')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(reverse('users:blogpost'))
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'home1.html', {'form': form, 'error': error})


def log_out(request):
    logout(request)
    return redirect(reverse('users:signup'))


def blogpost(request):
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
            return JsonResponse({'statusCode': 200, 'message': "Inserted Successfully"})
            #return redirect(reverse('users:blogpost'))
                #render(request, 'blogpost.html', {'form': details, 'error': error})
    else:
        form = PostForm()
        return render(request, 'blogpost.html', {'form': form, 'error': error})

    return redirect(reverse('users:blogpost'))


def index1(request):
    return render(request, 'index1.html')


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
            return JsonResponse({'statusCode': 200, 'message': "Updated Successfully"})
            #return redirect(reverse('users:myblog'))
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
            return JsonResponse({'statusCode': 200, 'message': "Deleted Successfully"})
            #return redirect(reverse('users:myblog'))
    else:
        form = PostForm(instance=obj)
        return render(request, "delete.html", {'form': form})


def admin_edit(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        post = PostForm(request.POST or None, instance=obj)
        if post.is_valid():
            post.save()
            return JsonResponse({'statusCode': 200, 'message': "Updated Successfully"})
            #return redirect(reverse('users:adminblog'))
    else:
        form = PostForm(instance=obj)
        return render(request, "adminedit.html", {'form': form})

def admin_delete(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        details = PostForm(request.POST or None, instance=obj)
        if details.is_valid():
            post = details.save(commit=False)
            post.is_deleted = True
            post.save()
            return JsonResponse({'statusCode': 200, 'message': "Deleted Successfully"})
            #return redirect(reverse('users:adminblog'))
    else:
        form = PostForm(instance=obj)
        return render(request, "admindelete.html", {'form': form})