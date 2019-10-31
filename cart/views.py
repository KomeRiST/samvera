from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Variaciya
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, var_id):
    cart = Cart(request)
    print("Получили корзину: ", cart)
    variaciya = get_object_or_404(Variaciya, id=var_id)
    print("Нашли вариацию: ", variaciya)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        print(".... форма валидна")
        cd = form.cleaned_data
        cart.add(variaciya=variaciya,
                 kolvo=cd['kolvo'],
                 update_kolvo=cd['update'])
        print(".... добавили товар в корзину.", cart)
    return redirect('cart:cart_detail')

def cart_remove(request, var_id):
    cart = Cart(request)
    variaciya = get_object_or_404(Variaciya, id=var_id)
    if variaciya is not None:
        cart.remove(str(variaciya.id))
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_kolvo_form'] = CartAddProductForm(
            initial={
                'kolvo': item['kolvo'],
                'update': True
            }
        )
    return render(request, 'cart/detail.html', {'cart': cart})