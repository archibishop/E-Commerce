from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy 

class SignUpForm(forms.Form):
    first_name = forms.CharField(label=ugettext_lazy('firstname'))
    last_name = forms.CharField(label=ugettext_lazy('lastname'))
    user_name = forms.CharField(label=ugettext_lazy('username'))
    email = forms.EmailField(label=ugettext_lazy('email'))
    password = forms.CharField(
        widget=forms.PasswordInput(), label=ugettext_lazy('password'))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label=ugettext_lazy('confirm password'))
    customer = forms.BooleanField(
        initial=False,  required=False, label=ugettext_lazy('customer'))

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    user_name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
    confirm_password.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('confirm_password')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Confirm Password and" +
                "Password should match.")

        user = User.objects.filter(username=cleaned_data
                            .get('user_name')).first()
        if user:
            raise forms.ValidationError("The username already " +
            "exists in the system.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=ugettext_lazy('Username'))
    password = forms.CharField(
        widget=forms.PasswordInput(), label=ugettext_lazy('password'))

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
