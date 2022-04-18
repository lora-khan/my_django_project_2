from django.shortcuts import render
from my_app.forms import UserForm, UserProfileInfoForm
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'my_app/index.html')


@login_required
def profile(request):
    return render(request, 'my_app/profile.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                print('found profile pic')
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'my_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('profile'))
            else:
                return HttpResponse('User is not active')
        else:
            print('someone tried to login your account and failed')
            print("user:{} pass:{}".format(username, password))
            return HttpResponse('Invalid password and username')

    else:
        return render(request, 'my_app/login.html', {})
