from .models import Users, User_details, Post
from .forms import RegistrationForm1, RegistrationForm2, LogInForm, PostForm
from . import views
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def signup1(request):
    # check if the request is post
    if request.method == 'POST':

        # Pass the form data to the form class
        details = RegistrationForm1(request.POST)

        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)

            # Finally write the changes into database
            post.save()

            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponse("data submitted successfully")

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


def signup2(request):
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
            return HttpResponse("Registered successfully")

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
            post.save()
            return redirect(reverse('users:index'))
                #render(request, 'index.html', {'form': details, 'error': error})
    else:
        form = PostForm()
        return render(request, 'index.html', {'form': form, 'error': error})

    return redirect(reverse('users:index'))



