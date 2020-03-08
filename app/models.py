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
from django.urls import reverse
from fabricator.models import consignment


class ColorField(models.CharField):
    """ Поле для хранения HTML-кода цвета."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(r'#[a-f\d]{6}'))


# Create your models here.
class PotentialClient(models.Model):
    first_name = models.CharField("Имя", max_length=30, help_text="Как к Вам обращаться?", default="Фамилия")
    last_name = models.CharField("Фамилия", max_length=30, help_text="Ваша фамилия", default="Фамилия")
    otch_name = models.CharField("Отчество", blank=True, max_length=30, help_text="Кто Вы по батьке?", default="")
    age = models.IntegerField("Возраст", help_text="Укажите Ваш возрат", default="22")
    email = models.EmailField("Эл. почта", help_text="Укажите Вашу электронную почту", default="example@mail.com")
    phone = models.IntegerField("Моб. тел.", help_text="Телефон для связи с Вами", default="89997776655")
    commet = models.TextField("", max_length = 255, blank=True, help_text="Укажите свои пожелания в одежде", default="Моё пожелание/описание одежды")

    data_create = models.DateTimeField("Дата регистрации", auto_now=True)

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

class Collection(models.Model):
    title = models.CharField("Название коллекции", db_index=True, max_length=50, help_text='Краткое название коллекции. Например: "Зима-Лето 2020"')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, help_text="url адресс данной коллекции", blank=True)
    data_create = models.DateField("Дата создания коллекции", auto_now_add=True)
    data_change = models.DateField("Дата изменения коллекции", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tovarbycollection', args=[self.slug])

    class Meta:
        ordering = ['-data_create',]
        verbose_name = "Коллекция товаров"
        verbose_name_plural = "Коллекции товаров"

class Category(models.Model):
    title = models.CharField("Название категории", db_index=True, max_length=50, help_text="(Например: Платья, юбки, костюмы)")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, help_text="url адресс данной категории", blank=True)
    data_create = models.DateField("Дата создания категории", auto_now_add=True)
    data_change = models.DateField("Дата изменения категории", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tovarbycategory', args=[self.slug])

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tovar(models.Model):
    kod = models.UUIDField(default=uuid.uuid1)
    title = models.CharField("Название изделия", db_index=True, max_length=50)
    slug = models.SlugField("url адресс товара", db_index=True, max_length=50, unique=True, blank=True)
    descr = models.TextField("Описание товара")
    uhod = models.TextField("Уход за изделием")
    sebestoimost = models.PositiveIntegerField("Себестоимость товара")
    cost = models.PositiveIntegerField("Цена для клиента", default=5000)
    data_create = models.DateField("Дата добавления товара", auto_now_add=True)
    hidden = models.BooleanField("Видимость для покупателя", help_text="Признак видимости товара на сайте", default=True)
    # have_vars = models.BooleanField("Наличие вариаций у товара", help_text="Признак видимости вариаций", default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='tovaritems', verbose_name='Категория товара')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True, default=1, related_name='collectionparts', verbose_name='В составе коллекции')

    def __str__(self):
        return self.title

    @property
    def random_image(self):
        v = Variaciya.objects.filter(tovar=self.id).order_by('?')[:1]
        # print (v[0].id)
        g = Gallery.objects.filter(product=v[0].id).order_by('?')[:1]
        if g.count() == 0:
            return "gallery/no_image.png"
        else:
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

    def get_absolute_url(self):
        return reverse('thing', args=[self.id, self.slug])

    class Meta:
        ordering = ['title']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"

class Variaciya(models.Model):
    tovar = models.ForeignKey(Tovar, on_delete=models.CASCADE, related_name='variacii')
    article = models.UUIDField(default=uuid.uuid4)
    #color = models.CharField("Цвет", max_length=7)
    #color = {
    #    ColorField: {'widget': forms.TextInput(attrs={'type': 'color'})}
    #}
    consignments = models.ManyToManyField(consignment)
    color = ColorField('Цвет материала', default='#FF0000')
    color_text = models.CharField("Название цвета", max_length=25, default='Красный')
    size = models.TextField("Размер", default="S")
    obmer = models.TextField("Обмеры")
    model = models.TextField("Параметры модели")
    count_sklad = models.IntegerField("Количество на складах", default=0, help_text="Считается автоматом при создании накладных и заказов")
    #image = models.ForeignKey(Gallery, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tovar.title} [{str(self.color_text)} | {str(self.size)}]'
    
    @property
    def kolvo(self):
        from django.db.models import Sum
        from orders.models import OrderItem
        prihod = self.in_variacii.all().aggregate(sum_var=Sum('kolvo'))
        if prihod['sum_var'] is None:
            prihod['sum_var'] = 0
        rashod = self.in_orders.all().aggregate(sum_var=Sum('count'))
        if rashod['sum_var'] is None:
            rashod['sum_var'] = 0

        return int(prihod['sum_var']) - int(rashod['sum_var'])

    def colortile(self):
        if self.color:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<div style="background-color: {0}; \
                height: 25px; width: 100px"></div>'.format(self.color))
        return 'пусто'
    
    def colortile_korz(self):
        if self.color:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<div id="color-{2}" data-var="{2}"><div style="background-color: {0};" class="color"></div> <small>({1})</small></div>'.format(self.color, self.color_text, self.id))
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

class MtoM_VarsToCons(models.Model):
    consignments = models.ForeignKey(consignment, on_delete=models.CASCADE, related_name="in_consignments")
    variacii = models.ForeignKey(Variaciya, on_delete=models.CASCADE, related_name="in_variacii")
    # gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, related_name="in_gallery")
    kolvo = models.SmallIntegerField("Количество", default=0)
    cost = models.SmallIntegerField("Цена", default=0)
    nds = models.SmallIntegerField("Ставка НДС (%)", default=0)
    nds_summ = models.SmallIntegerField("Сумма НДС (руб.)", default=0)
    total_not_nds = models.SmallIntegerField("Сумма без НДС", default=0)
    total_nds = models.SmallIntegerField("Сумма с учётом НДС", default=0)
    count_added = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if (self.count_added == 0) or (self.count_added == None):
            # r = self.variacii.count_sklad + self.kolvo
            # self.variacii.update(count_sklad=r)
            var = Variaciya.objects.get(pk=self.variacii.id)
            var.count_sklad += self.kolvo
            var.save()
            self.count_added = True
        super(MtoM_VarsToCons, self).save(*args, **kwargs)
                                                                                                                                                                                                                    
    def delete(self, *args, **kwargs):
        if self.count_added == 1:
            var = Variaciya.objects.get(pk=self.variacii.id)
            var.count_sklad -= self.kolvo
            var.save()
        super(MtoM_VarsToCons, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Позиция накладной"
        verbose_name_plural = "Состав накладной"

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
        verbose_name = "Фото вариации"
        verbose_name_plural = "Фотографии вариации"

