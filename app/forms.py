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
            
    adress = forms.CharField(label=_("Адрес доставки"),
                            widget=forms.TextInput({
                                   'type': 'text',
                                   'class': 'form-control',
                                   'placeholder': 'Адрес доставки'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

################################
#
#
#    Формы для своей админки   #
#
#
################################


class ThingEditForm(forms.ModelForm):

    class Meta:
        model = models.Tovar
        fields = ['title', 'descr', 'uhod', 'sebestoimost', 'cost', 'hidden']
        
class VariaciyaEditForm(forms.ModelForm):
    from app.models import ColorField
    color = forms.CharField(widget=forms.TextInput({
                    'type': 'color',
                    'style': 'height: 25px; width: 100px'})
                )
    size = forms.CharField(max_length=50, label=_("Размер"))

    class Meta:
        model = models.Variaciya
        fields = ['color', 'color_text', 'size', 'obmer', 'model', 'kolvo']

class VarPhotoForm(forms.ModelForm):

    class Meta:
        model = models.Gallery
        fields = ['image']