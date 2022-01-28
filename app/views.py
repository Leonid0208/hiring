from django.shortcuts import render
from .forms import *
from django.shortcuts import redirect
from django.urls import reverse


def main(request):
    return render(request, 'app/main.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return render(request, 'registration/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            user_form = CustomUserCreationForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                # new_user = User.objects.create(email=email, password=password)
                new_user = user_form.save(commit=False)
                # Set the chosen password
                # new_user.set_password(user_form.cleaned_data['password'])
                # new_user.username = new_user.email
                # Save the User object
                new_user.save()
                return redirect('login')
            else:
                render(request, 'registration/register.html', {'form': user_form, 'message': 'Wrong data'})
        else:
            user_form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': user_form})




