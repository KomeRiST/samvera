"""
Definition of models.
"""

from django.db import models
import datetime
import uuid
from django import forms
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

class ColorField(models.CharField):
    """ Поле для хранения HTML-кода цвета."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(r'#[a-f\d]{6}'))


class StatusOrder(models.Model):
    kod = models.PositiveIntegerField("Код статуса", unique=True)
    text = models.TextField("Текстовое представление статуса")

# Create your models here.
class PotentialClient(models.Model):
    first_name = models.CharField("Имя", max_length=30, help_text="Как к Вам обращаться?", default="Фамилия")
    last_name = models.CharField("Фамилия", max_length=30, help_text="Ваша фамилия", default="Фамилия")
    otch_name = models.CharField("Отчество", blank=True, max_length=30, help_text="Кто Вы по батьке?", default="")
    age = models.IntegerField("Возраст", help_text="Укажите Ваш возрат", default="22")
    email = models.EmailField("Эл. почта", help_text="Укажите Вашу электронную почту", default="example@mail.com")
    phone = models.IntegerField("Моб. тел.", help_text="Телефон для связи с Вами", default="89997776655")
    commet = models.TextField("", max_length = 255, blank=True, help_text="Укажите свои пожелания в одежде", default="Моё пожелание/описание одежды")

    data_create = models.DateTimeField("Дата регистрации", default=datetime.datetime.now())

    class Meta:
        verbose_name = "Потенциальный клиент"
        verbose_name_plural = "Потенциальные клиенты"

class Orders(models.Model):
    ''' Таблица заказов. Запись создается после подтверждения заказа в корзине '''
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(StatusOrder, on_delete=models.DO_NOTHING)
    namber = models.UUIDField(default=uuid.uuid4)
    date_create = models.DateField("Дата создания заявки", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка клиента"
        verbose_name_plural = "Заявки клиентов"

class OrderTovary(models.Model):
    ''' Таблица товаров из заказа '''
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    tovar = models.ForeignKey('Tovar', on_delete=models.DO_NOTHING)
    #count = models.PositiveIntegerField("Количество товара")

    class Meta:
        verbose_name = "Товар Заказа"
        verbose_name_plural = "Товары заказов"
        
class OrderTovaryVariaciya(models.Model):
    ''' Таблица вариаций для товара из заказа '''
    ordertovar = models.ForeignKey(OrderTovary, on_delete=models.CASCADE)
    variaciya = models.ForeignKey('Variaciya', on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField("Количество товара")

    class Meta:
        verbose_name = "Вариация товара"
        verbose_name_plural = "Выриации товаров"

class Tovar(models.Model):
    kod = models.UUIDField(default=uuid.uuid1)
    title = models.CharField("Нозвание изделия", max_length=50)
    descr = models.TextField("Описание товара")
    uhod = models.TextField("Уход за изделием")
    sebestoimost = models.PositiveIntegerField("Себестоимость товара")
    cost = models.PositiveIntegerField("Цена для клиента", default=5000)
    data_create = models.DateField("Дата добавления товара", auto_now_add=True)
    hidden = models.BooleanField("Видимость для покупателя", help_text="Признак видимости товара на сайте", default=True)

    def __str__(self):
        return self.title

    @property
    def random_image(self):
        v = Variaciya.objects.filter(tovar=self.id).order_by('?')[:1]
        print (v[0].id)
        g = Gallery.objects.filter(product=v[0].id).order_by('?')[:1]
        return g[0].image

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"

class Variaciya(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='tovar')
    article = models.UUIDField(default=uuid.uuid4)
    color = {
        ColorField: {'widget': forms.TextInput(attrs={'type': 'color'})}
    }
    size = models.TextField("Размер", default="S")
    obmer = models.TextField("Обмеры")
    model = models.TextField("Параметры модели")
    #image = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tovar.title} [{str(self.color)} | {str(self.size)}]'
    
    @property
    def random_image(self):
        v = Variaciya.objects.filter(tovar=self.id).order_by('?')[:1]
        print (v[0].id)
        g = Gallery.objects.filter(product=v[0].id).order_by('?')[:1]
        return g[0].image

    class Meta:
        verbose_name = "Вариация товара"
        verbose_name_plural = "Вариации товаров"

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    product = models.ForeignKey(Variaciya, on_delete=models.CASCADE, related_name="gallery")

