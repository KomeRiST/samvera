"""
Definition of models.
"""

from django.core import validators
from django.db import models
from django.db.models import Count
import datetime
import uuid
from django import forms
from samvera import settings
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.utils.safestring import mark_safe

class ColorField(models.CharField):
    """ Поле для хранения HTML-кода цвета."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(r'#[a-f\d]{6}'))


class StatusOrder(models.Model):
    kod = models.PositiveIntegerField("Код статуса", unique=True)
    text = models.TextField("Текстовое представление статуса")
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Справочник статусов заказа"

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

# class Orders(models.Model):
#     ''' Таблица заказов. Запись создается после подтверждения заказа в корзине '''
#     client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     status = models.ForeignKey(StatusOrder, on_delete=models.DO_NOTHING)
#     namber = models.UUIDField(default=uuid.uuid4)
#     date_create = models.DateField("Дата создания заявки", auto_now_add=True)

#     class Meta:
#         verbose_name = "Заявка клиента"
#         verbose_name_plural = "Заявки клиентов"

# class OrderTovary(models.Model):
#     ''' Таблица товаров из заказа '''
#     order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="tovary")
#     tovar = models.ForeignKey('Tovar', on_delete=models.DO_NOTHING, related_name="in_orders")
#     #count = models.PositiveIntegerField("Количество товара")

#     class Meta:
#         verbose_name = "Заказанное изделие"
#         verbose_name_plural = "Заказанные изделия"
        
# class OrderTovaryVariaciya(models.Model):
#     ''' Таблица вариаций для товара из заказа '''
#     order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="ordervars")
#     ordertovar = models.ForeignKey(OrderTovary, on_delete=models.CASCADE, related_name="variacii")
#     variaciya = models.ForeignKey('Variaciya', on_delete=models.DO_NOTHING, related_name="in_orders")
#     count = models.PositiveIntegerField("Количество товара")

#     def summ(self):
#         return str(self.count * self.variaciya.tovar.cost)+' р.'

#     class Meta:
#         verbose_name = "Вариация товара из заявки"
#         verbose_name_plural = "Вариации товаров из заявок"

class Category(models.Model):
    title = models.CharField("Название категории")

class Tovar(models.Model):
    kod = models.UUIDField(default=uuid.uuid1)
    title = models.CharField("Название изделия", max_length=50)
    descr = models.TextField("Описание товара")
    uhod = models.TextField("Уход за изделием")
    sebestoimost = models.PositiveIntegerField("Себестоимость товара")
    cost = models.PositiveIntegerField("Цена для клиента", default=5000)
    data_create = models.DateField("Дата добавления товара", auto_now_add=True)
    hidden = models.BooleanField("Видимость для покупателя", help_text="Признак видимости товара на сайте", default=True)
    category = 

    def __str__(self):
        return self.title

    @property
    def random_image(self):
        v = Variaciya.objects.filter(tovar=self.id).order_by('?')[:1]
        # print (v[0].id)
        g = Gallery.objects.filter(product=v[0].id).order_by('?')[:1]
        return g[0].image

    def count_var(self):
        vars = Variaciya.objects.filter(tovar=self)
        return vars.count()
    count_var.short_description = 'Кол-во вариаций'
    
    def sizes(self):
        s = ""
        vs = self.variacii.values('size').annotate(Count('id')).order_by()
        print("vs = ", vs)
        for i in vs:
            print("I = ", i)
            sz = i['size']
            s=s+f'<div id="size-{sz}" data-tovar="{self.id}" data-size="{sz}" style="padding: .5rem; background: 1px solid gray; border-radius: .5rem;">{sz}</div>'
        return s

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"

class Variaciya(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='variacii')
    article = models.UUIDField(default=uuid.uuid4)
    #color = models.CharField("Цвет", max_length=7)
    #color = {
    #    ColorField: {'widget': forms.TextInput(attrs={'type': 'color'})}
    #}
    color = ColorField('Цвет материала', default='#FF0000')
    color_text = models.CharField("Название цвета", max_length=25, default='Красный')
    size = models.TextField("Размер", default="S")
    obmer = models.TextField("Обмеры")
    model = models.TextField("Параметры модели")
    kolvo = models.SmallIntegerField("Количество на складах", default=0)
    #image = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tovar.title} [{str(self.color_text)} | {str(self.size)}]'
    
    def colortile(self):
        if self.color:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<div style="background-color: {0}; \
                height: 25px; width: 100px"></div>'.format(self.color))
        return 'пусто'
    
    def colortile_korz(self):
        if self.color:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<div id="color-{2}" data-var="{2}"><div style="background-color: {0};height: 24px;width: 24px;margin: auto;" class="color"></div> <small>({1})</small></div>'.format(self.color, self.color_text, self.id))
        return 'пусто'

    def size_tag(self):
        from django.utils.safestring import mark_safe
        return mark_safe(f'<div id="size-{self.size}" data-tovar="{self.tovar.id}" data-size="{self.size}" style="padding: .5rem; background: 1px solid gray; border-radius: .5rem;">{self.size}</div>')

    @property
    def random_image(self):
        #v = Variaciya.objects.filter(tovar=self.id)[:1]
        #print (v[0].id)
        g = Gallery.objects.filter(product=self)[:1]
        if g.count() == 0:
            return mark_safe(u'<img src="{0}{1}" width="100"/>'.format(settings.MEDIA_URL, "gallery/no_image.png"))
        return mark_safe(u'<img src="{0}{1}" width="100"/>'.format(settings.MEDIA_URL,g[0].image))

    @property
    def images(self):
        i = Gallery.objects.filter(pk=self.pk)
        return i
    
    #def image_img(self):
    #    imgs = self.images
    #    if imgs:
    #        from django.utils.safestring import mark_safe
    #        s = ""
    #        for i in imgs:
    #            s = s + mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(i.image.url))
    #        return s
    #    else:
    #        return '(Нет изображения)'
    #image_img.short_description = 'Картинка'
    #image_img.allow_tags = True

    class Meta:
        verbose_name = "Вариация изделия"
        verbose_name_plural = "Вариации изделий"

class Korzina(Variaciya):
    def __init__(self):
        # Необходимо вызвать метод инициализации родителя.
        # В Python 3.x это делается при помощи функции super()
        super().__init__()
        
    #v = models.ForeignKey(Variaciya, on_delete=models.DO_NOTHING)

    count = models.SmallIntegerField("Количество")
    summ = models.SmallIntegerField("Сумма")

    #@property
    #def summ(self):
    #    s = self.count * self.tovar.cost
    #    return str(s)

    class Meta:
        managed = False


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    product = models.ForeignKey(Variaciya, on_delete=models.CASCADE, related_name="gallery")
    # Вывод картинок в админке!
    def image_img(self):
        if self.image:
            return mark_safe(u'<img src="{0}" width="100"/>'.format(self.image.url))
        else:
            return mark_safe(u'<img src="{0}" width="100"/>'.format("gallery/no_image.png"))
    image_img.short_description = 'Картинка'
    image_img.allow_tags = True
    class Meta:
        verbose_name = "Галлерея вариации"
        verbose_name_plural = "Галлереи вариаций"

