from django.contrib.auth.models import User
from django import forms

class OrderForm(forms.ModelForm):
    phone = forms.CharField(label=("Телефон"),
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