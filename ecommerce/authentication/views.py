from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Person
from django.views import View
from .forms import SignUpForm, LoginForm

# Create your views here.
def index(request):
    return render(request, 'main_page.html')


class SignUp(View):
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = create_user(form)
            Person.objects.create(user=user, customer=form.cleaned_data.get(
                'customer'))
            login(request, user)
            messages.success(request, 'You have been successfully logged in')
            return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, {'form': form})


class Login(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'You have successfully Logged In')
                return HttpResponseRedirect(reverse('product:product-list'))
        messages.error(request, 'User does not exist. Wrong Email/Password')
        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(
            request, 'You have logged out of the system.')
        return HttpResponseRedirect(reverse('product:product-list'))


def create_user(form):
    user = User.objects.create_user(username=form.cleaned_data.get(
        'user_name'),
        email=form.cleaned_data.get(
        'email'),
        password=form.cleaned_data.get(
        'password'),
        first_name=form.cleaned_data.get(
        'first_name'),
        last_name=form.cleaned_data.get(
        'last_name'))
    return user
