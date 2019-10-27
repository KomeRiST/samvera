from django.db import models

# Create your models here.
# class Order(models.Model):
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
        
# class OrderItem(models.Model):
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
