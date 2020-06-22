from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from .models import Profile

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:

            qs = User.objects.filter(username=username)
            qs_email = User.objects.filter(email=username)

            qs = qs.union(qs_email)
            print(username, qs, qs_email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!!!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Этот пользователь неактивен')
        return super(UserLoginForm, self).clean()


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Никнейм', widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Как к вам обращаться?', widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
                                attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
                                attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!!')
        return data['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
