from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Person
from django.views import View
from .forms import SignUpForm, LoginForm
from django.utils.translation import gettext
from django.utils import translation

# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('product:product-list'))


class SignUp(View):
    form_class = SignUpForm
    template_name = 'sign_up.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            customer = form.cleaned_data.get(
                'customer')
            user = create_user(form)
            Person.objects.create(user=user, customer=customer)
            login(request, user)
            message_output = gettext('You have been successfully logged in.')
            messages.success(request, message_output)
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
                message_output = gettext(
                    'You have successfully Logged In.')
                messages.success(
                    request, message_output)
                return HttpResponseRedirect(reverse('product:product-list'))
        message_output = gettext('User does not exist. Wrong Email/Password.')
        messages.error(request, message_output)
        return render(request, self.template_name, {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        message_output = gettext('You have logged out of the system.')
        messages.info(
            request, message_output)
        return HttpResponseRedirect(reverse('product:product-list'))


class Language(View):
    def get(self, request, *args, **kwargs):
        user_language = kwargs['language']
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        message_output = gettext('You have changed the language.')
        messages.info(request, message_output)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER',''),)


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
