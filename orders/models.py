from django.db import models
from app import models as m
import uuid
from django.contrib.auth.models import User

class Order(models.Model):
    ''' Таблица заказов. Запись создается после подтверждения заказа в корзине '''
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    addres = models.TextField("Адрес доставки")
    status = models.ForeignKey(m.StatusOrder, on_delete=models.DO_NOTHING)
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
    variaciya = models.ForeignKey(m.Variaciya, on_delete=models.DO_NOTHING, related_name="in_orders")
    cost = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField("Количество товара")

    def summ(self):
        return str(self.count * self.cost)+' р.'

    class Meta:
        verbose_name = "Вариация товара из заявки"
        verbose_name_plural = "Вариации товаров из заявок"
