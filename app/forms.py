"""
Definition of forms.
"""

from django import forms
from app import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class Form_PotentialClient(forms.ModelForm):
    class Meta:
        model = models.PotentialClient
        exclude = ['data_create']

class FormGallery(forms.ModelForm):
    class Meta:
        model = models.Gallery
        fields = "__all__"

class FormKorzina(forms.ModelForm):
    count = forms.NumberInput()
    image = forms.ImageField()

    class Meta:
        model = models.Variaciya
        fields = ['tovar', 'size', 'color']

class OrderForm(forms.ModelForm):
    phone = forms.CharField(label=_("Телефон"),
                            max_length=11,
                               widget=forms.TextInput({
                                   'type': 'tel',
                                   'class': 'form-control',
                                   #'pattern':'8([0-9]{3})-[0-9]{3}-[0-9]{2}-[0-9]{2}',
                                   'placeholder': '8(___)___-____'}))

    first_name = forms.CharField(max_length=50,
                               widget=forms.TextInput({
                                   'type': 'text',
                                   'class': 'form-control',
                                   'placeholder': 'Имя Отчество'}))

    last_name = forms.CharField(max_length=50,
                               widget=forms.TextInput({
                                   'type': 'text',
                                   'class': 'form-control',
                                   'placeholder': 'Фамилия'}))

    email = forms.CharField(widget=forms.TextInput({
                                   'type': 'email',
                                   'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']