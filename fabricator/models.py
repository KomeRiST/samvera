from django.db import models
from django.urls import reverse
# from app.models import Variaciya, Tovar, Gallery

# Create your models here.
class fabricator(models.Model):
    '''
    Объект производителя
    '''
    title = models.CharField("Наименование производителя", db_index=True, max_length=50, help_text="Название ООО или ИП или если частник, то просто ФИО")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, help_text="url адрес страницы производителя")
    address = models.CharField("Адрес места производства", max_length=100, help_text="Адрес в свободной форме (макс 100 символов)")
    contacts = models.CharField("Контакты производителя", max_length=100, help_text="Контакты в свободной форме (макс 100 символов)")
    data_create = models.DateField("Дата создания производителя", auto_now_add=True)
    data_change = models.DateField("Дата изменения производителя", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reversed('fabricator', args=[self.slug])
    
    class Meta:
        ordering = ['title']
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
    
class consignment(models.Model):
    '''
    Накладная
    '''
    closed = models.BooleanField("Документ закрыт", default=False, help_text="Еслди документ закрыт, то он обрабатывается системой.")
    number = models.CharField("Номер накладной", db_index=True, max_length=25, help_text="Это поле соответствует номеру документа")
    data_doc = models.DateField("Дата документа")
    fabricator = models.ForeignKey(fabricator, on_delete=models.DO_NOTHING, related_name="items")
    #variaciyi = models.ManyToManyField(Variaciya, related_name="consignments")
    #tovary = models.ManyToManyField(Tovar, related_name="tovar_consignments")
    #gallery = models.ManyToManyField(Gallery, related_name="gallery_consignments")
    responsible = models.CharField("Ответственнное лицо", max_length=50, help_text="ФИО ответственного за производство товара")
    data_create = models.DateField("Дата создания документа в системе", auto_now_add=True)
    data_change = models.DateField("Дата изменения докумета в системе", auto_now=True)

    def __str__(self):
        return f'№ {self.number} от {self.data_doc}'

    class Meta:
        ordering = ['-data_doc']
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"