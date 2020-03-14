from django.db import models
from app.models import Variaciya
import uuid
from django.contrib.auth.models import User


class StatusOrder(models.Model):
    kod = models.PositiveIntegerField("Код статуса", unique=True)
    text = models.TextField("Текстовое представление статуса")
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Справочник статусов заказа"

class Order(models.Model):
    ''' Таблица заказов. Запись создается после подтверждения заказа в корзине '''
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    addres = models.TextField("Адрес доставки")
    status = models.ForeignKey(StatusOrder, on_delete=models.DO_NOTHING)
    # namber = models.UUIDField(default=uuid.uuid4)
    date_create = models.DateField("Дата создания заявки", auto_now_add=True)
    date_update = models.DateField("Дата обновления заявки", auto_now=True)

    class Meta:
        ordering = ('-date_create',)
        verbose_name = "Заявка клиента"
        verbose_name_plural = "Заявки клиентов"
    
    def __str__(self):
        return 'Заказ: {}'.format(self.id)

# class OrderTovary(models.Model):
#     ''' Таблица товаров из заказа '''
#     order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="tovary")
#     tovar = models.ForeignKey('Tovar', on_delete=models.DO_NOTHING, related_name="in_orders")
#     #count = models.PositiveIntegerField("Количество товара")

#     class Meta:
#         verbose_name = "Заказанное изделие"
#         verbose_name_plural = "Заказанные изделия"
        
class OrderItem(models.Model):
    ''' Таблица вариаций для товара из заказа '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordervars")
    # ordertovar = models.ForeignKey(OrderTovary, on_delete=models.CASCADE, related_name="variacii")
    variaciya = models.ForeignKey(Variaciya, on_delete=models.DO_NOTHING, related_name="in_orders")
    cost = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField("Количество товара")
    count_added = models.BooleanField("Учтено в подсчёте количества или нет?", default=False)

    def summ(self):
        return str(self.count * self.cost)

    @property
    def summ_item(self):
        return self.count * self.cost

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)
        if self.count_added == False:
            var = Variaciya.objects.get(pk=self.variaciya)
            var.count_sklad -= self.count
            var.save()
        
    def delete(self, *args, **kwargs):
        if self.count_added == True:
            var = Variaciya.objects.get(pk=self.variaciya)
            var.count_sklad += self.count
            var.save()
        super(OrderItem, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Вариация товара из заявки"
        verbose_name_plural = "Вариации товаров из заявок"
