from decimal import Decimal
from django.conf import settings
from app.models import Variaciya

class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) # Попытка получения корзины с текущей сессии пользователя
        if not cart: # Если корзины в сесси нет, то создаём пустую
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variaciya, kolvo = 1, update_kolvo = False):
        """
        Добавить товар в корзину или обновить его количество
        """
        var_id = str(variaciya.id)
        if var_id not in self.cart:
            print("Не нашли вариацию: ", var_id)
            self.cart[var_id] = {'kolvo': 0,
                                 'cost': str(variaciya.tovar.cost)}
            print("    добавили вариацию: ", self.cart[var_id])
        if update_kolvo:
            self.cart[var_id]['kolvo'] = kolvo
        else:
            self.cart[var_id]['kolvo'] += kolvo
        self.save()

    def save(self):
        """
        Обновление сессии
        """
        self.session[settings.CART_SESSION_ID] = self.cart # Обновляем свою переменную в сессии пользователя
        self.session.modified = True # Отмечаем сессию как "изменённую", чтобы убедиться в сохранении данных

    def remove(self, var_id):
        """
        Удаление товара из корзины
        """
        #var_id = str(variaciya.id)
        if var_id in self.cart:
            del self.cart[var_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение товаров из БД.
        """
        var_ids = self.cart.keys()
        vars = Variaciya.objects.filter(id__in=var_ids)
        for item in vars:
            self.cart[str(item.id)]['variaciya'] = item

        for item in self.cart.values():
            item['cost'] = Decimal(item['cost'])
            item['summ'] = item['cost'] * item['kolvo']
            yield item

    def __len__(self):
        """
        Подсчёт всех товаров в корзине
        """
        return sum(item['kolvo'] for item in self.cart.values())

    def get_total_summ(self):
        """
        Подсчёт стоимости товаров в корзине.
        """
        return sum(Decimal(item['cost']) * item['kolvo'] for item in self.cart.values())

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True