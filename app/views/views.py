"""
Definition of views.
"""
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from app import forms, models, base_auth
from orders.models import Order
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum
from django.forms import formset_factory
import json
from django.core import serializers
from django.template.loader import render_to_string

def year():
    return "2019 - " + str(datetime.now().year)

def login(request):
    """  """
    assert isinstance(request, HttpRequest)
    print("request.method: ", request.method)
    if request.method == "GET":
        print("Чел не авторизован!")
        return render(
            request,
            'app/account/login.html',
            {
                'title':'Авторизация',
                'form':forms.BootstrapAuthenticationForm,
                'year':year(),
            }
        )
    else:
        from django.contrib.auth import authenticate
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request)
                print("Чел авторизовлся.\n")
                print("HTTP_REFERER: ", request.META["HTTP_REFERER"])
                return HttpResponseRedirect("/kabinet/")
                # Redirect to a success page.
            else:
                print("disabled account.\n")
                # Return a 'disabled account' error message
                return HttpResponseRedirect("/")
        else:
            # Return an 'invalid login' error message.
            print("invalid login. \n")
            return render(
                request,
                'app/account/login.html',
                {
                    'title':'Авторизация',
                    'form':forms.BootstrapAuthenticationForm,
                    'year':year(),
                }
            )

#def viktoleon(request):
#    """Рендер админки для Вики"""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/account/viktoleon.html',
#        {
#            'title':'Home Page',
#            'year':year(),
#        }
#    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    #try:
    #    tovarfolder = base_auth.zapros("получить","группы_товаров")
    #except :
    #    send_mail("Новый потеннциальный клиент",
    #                 f"Ошибка при запросе получения категорий товаров!",
    #                 'komerist@bk.ru', 
    #                 ['komerist1993-93@mail.ru','komerist@bk.ru'], )
    #    tovarfolder = {}

    #try:
    #    kollections = base_auth.zapros("получить","коллекции")
    #    pass
    #except :
    #    send_mail("Новый потеннциальный клиент",
    #                 f"Ошибка при запросе получения коллекций!",
    #                 'komerist@bk.ru', 
    #                 ['komerist1993-93@mail.ru','komerist@bk.ru'], )
    #    kollections = {}
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            # 'categories' : models.Category.objects.all(),
            #'tovarfolder': tovarfolder,
            #'kollections': kollections,
            'year':year(),
            #'Form_PotentialClient': forms.Form_PotentialClient,
        }
    )

def tovarlist(request, category_slug=None):
    template = 'app/catalog/catalog.html'
    context = {}
    category = None
    # categories = models.Category.objects.all()
    tovary = models.Tovar.objects.filter(hidden=True, variacii__count_sklad__gt = 0, variacii__in_variacii__consignments__closed = True)
    if category_slug:
        category = get_object_or_404(models.Category, slug=category_slug)
        tovary = tovary.filter(category=category)
    context['category'] = category
    context['tovary'] = tovary
    # context['categories'] = categories
    return render(
        request,
        template,
        context,
    )

def tovarlist_collection(request, collection_slug=None):
    template = 'app/catalog/catalog.html'
    context = {}
    coll = None
    # categories = models.Category.objects.all()
    tovary = models.Tovar.objects.filter(hidden=True, variacii__count_sklad__gt = 0, variacii__in_variacii__consignments__closed = True)
    if collection_slug:
        coll = get_object_or_404(models.Collection, slug=collection_slug)
        tovary = tovary.filter(collection=coll)
    context['collection'] = coll
    context['tovary'] = tovary
    # context['categories'] = categories
    return render(
        request,
        template,
        context,
    )

def thing(request, id, slug):
    """Карточка товара"""
    t = get_object_or_404(models.Tovar, pk=id, slug=slug, hidden=True, variacii__in_variacii__consignments__closed = True)
    assert isinstance(request, HttpRequest)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'app/catalog/thing.html',
        {
            'message':t.title,
            'thing': t,
            'title':'Карточка товара',
            'year':year(),
            'cart_product_form': cart_product_form
        }
    )

def kabinet(request):
    """Страница личного кабинета юзера со всеми его заказами."""
    if request.user.is_authenticated:
        title = "Личный кабинет"
        message = "Посмотрите исторю своих покупок, а также статус текущих заказов."
        orders = Order.objects.filter(client=request.user.id)
        page = 'app/account/lk.html'
        assert isinstance(request, HttpRequest)
        return render(
            request,
            page,
            {
                'title':title,
                'message':message,
                'orders':orders,
                'year':year(),
            }
        )
    else:
        from django.contrib.auth.forms import AuthenticationForm
        title="Вход на сайт"
        message="Введите свои данные для входа на сайт"
        page = 'app/account/login.html'
        orders=None
        assert isinstance(request, HttpRequest)
        return render(
            request,
            page,
            {
                'title':title,
                'message':message,
                'form':AuthenticationForm,
                'year':year(),
            }
        )

def getthingcolors(request, tovar, size):
    """Формирование HTML кода с вариантами цветов товара"""
    t = get_object_or_404(models.Tovar, pk=tovar)
    print("tovar = ", t)
    r = t.variacii.filter(size=size) #, kolvo__gt=0)
    print("FILTER SIZE = ", r)
    st = ""
    for v in r:
        st = st + v.colortile_korz()
    assert isinstance(request, HttpRequest)
    return HttpResponse(st)

def getthingphtotoss(request, variaciya):
    """Формирование HTML кода с фотками вариации товара"""
    v = get_object_or_404(models.Variaciya, pk=variaciya)
    print("variaciya = ", v)
    r = v.gallery.all()
    st = ""
    for i in r:
        st = st + f'<div class="carousel-cell" ><img src="/media/{i.image}" alt=""/></div>'
    res={}
    res['img']=st
    res['id']=v.id
    res['model']=v.model
    res['obmer']=v.obmer
    kol = v.kolvo + 1
    for i in range(1, kol, 1):
        st = st + f'<option value="{i}">{i}</option>'
    res['kolvo']=st
    # <option value="1">1</option>
    assert isinstance(request, HttpRequest)
    return HttpResponse(json.dumps(res))

def post(request, code):
    if request.method == 'POST':
        form = forms.Form_PotentialClient(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            l = models.PotentialClient.objects.filter(phone=p.phone).count()
            if l == 0:
                p.save()
                send_mail("Новый потеннциальный клиент", f"ФИО {p.first_name} {p.last_name} {p.otch_name}\n\
                Возраст {p.age}\n\
                Email {p.email}\n\
                Тел. {p.phone}\n\
                Коммент {p.commet}\n", 'komerist@bk.ru', ['komerist1993-93@mail.ru','komerist@bk.ru', 'viktoleon@bk.ru'], )
            return HttpResponse(f'Всего записей: {l}')
    return httpresponseredirect('/')

def new_order(request):
    """ Рендер страницы подтверждения заказа """
    if request.POST:

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")


        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/good_order.html',
            {
                'title':'Спасибо за оформление заказа<br/>Номер Вашего заказа: {{number_order}}',
                'message':f'В ближайшее время с Вами свяжутся для подтверждения заказа {email}',
                'year':year(),
            }
        )
    else:
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/new_order.html',
            {
                'title':'Оформление заказа',
                'message':'Проверте состав заказа, введите реквизиты и подтвердите оформление заказа',
                'form': forms.OrderForm,
                'korzina': request.GET.get("korzina"),
                'year':year(),
            }
        )
    
def get_order(request):
    """ Рендер страницы подтверждения заказа """
    if request.method == 'POST':
        user_pass = ''
        phone = request.POST['phone']
        print (phone)
        import re
        re.sub('\ |(|)|-', '', phone)
        print (phone)
        try:
            # Проверить пользователя по его телефону
            user = User.objects.get(username = phone, email = request.POST['email'])
        except ObjectDoesNotExist:
            # Создать пользователя
            user_pass =  User.objects.make_random_password()
            user = User.objects.create_user(phone, request.POST['email'], user_pass)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            from django.core.mail import EmailMessage
            email = EmailMessage("Регистрация на www.samvera.ru", f"{user.last_name}!\n\
                    Ваш почтовый адресс был указан при регистрации на сайте www.samvera.ru\n\
                    \n\
                    Для входа на сайт используйте следующие данные:\n\
                    Страница входа: <a href='www.samvera.ru\kabinet\'>www.samvera.ru</a>\n\
                    Страница входа: www.samvera.ru\kabinet\ \n\
                    Логин: {user.username} или {user.email}\n\
                    Пароль: {user_pass}", to=['komerist1993-93@mail.ru','komerist@bk.ru'])
            email.send()
            
        # Создать заказ
        order = models.Orders()
        order.client = user
        order.status = models.StatusOrder.objects.get(id=2) # Принят в обработку
        order.save()
        korz = request.POST['korzina']

        # korz = [{'count': '1', 'id': 1}, {'count': '2', 'id': 2}]
        korz = json.loads(korz)
        for item in korz:
            pass
            #print("цикл: ", ids[x])
            try:
                if item['id'] != '':
                    t=models.Variaciya.objects.get(id=int(item['id']))


                    ordertovarvariaciya = models.OrderTovaryVariaciya()

                    ordertovar, created = models.OrderTovary.objects.get_or_create(order=order, tovar=t.tovar)
                    ordertovarvariaciya.order = order
                    ordertovarvariaciya.ordertovar = ordertovar

                    ordertovarvariaciya.variaciya = t
                    ordertovarvariaciya.count = int(item['count'])
                    ordertovarvariaciya.save()

                else:
                    ids.pop(x)

            except ObjectDoesNotExist:
                print("Either the entry or blog doesn't exist.")
                ids.pop(x)

#, 'slviktoleon@yandex.ru'
        # Отправить на почту оператора состав заказа с реквизитами клиента для связи с ним и пдт заказа. , 'viktoleon@bk.ru'
        html_message = render_to_string(
            'app/email-order_template.html',
            {
                'order': order,
                'user': user,
            }
        )
        print("html_message = \n")
        print(html_message)
        send_mail("Новая заявка!!!", f"ФИО {user.last_name} {user.first_name}\n\
                Email {user.email}\n\
                Тел. {user.username}\n\
                \n\
                Номер заказа: {order.namber}\n\
                ", 'komerist@bk.ru', ['komerist1993-93@mail.ru'], html_message=html_message)
#, 'viktoleon@bk.ru'
        # Отправить на почту клиенту уведомление о формировании заказа.
        from django.contrib import messages
        messages.success(request, 'Profile updated successfully')
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/good_order.html',
            {
                'title':'Заказ принят на обработку',
                'message':'Спасибо за оформление заказа. С Вами скоро свяжутся.',
                'mess': html_message,
                'year':year(),
            }
        )
    else:
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/new_order.html',
            {
                'title':'Оформление заказа',
                'message':'Введите реквизиты и подтвердите оформление заказа',
                'form': forms.OrderForm,
                'korzina': request.GET.get("korzina"),
                'year':year(),
            }
        )


from cart.forms import CartAddProductForm


def product_detail(request, id, slug):
    variaciya = get_object_or_404(models.Variaciya,
                                id=id,
                                tovar__hidden=False)
    cart_product_form = CartAddProductForm()
    return render(request, 'app/catalog/thing.html', {'variaciya': variaciya,
                                                        'cart_product_form': cart_product_form})

def korzina_get(request):
    """Рендер куска кода HTML для вставки в шаблон страницы Корзина"""
    print ("body^ ", request.GET)
    gt = request.GET.get('korzina')
    print(gt)
    spl = gt.split('|')
    ids = spl[0]
    print(ids)
    cts = spl[1]
    print(cts)
    cts=cts.split(',')
    ids=ids.split(',')
    x=len(cts)-1
    itog=0
    msg = []
    #korz = models.Variaciya.objects.filter(id__in=map(float, arr.split(',')))
    #tovary = models.Variaciya.objects.filter(id__in=map(int, arr.split(','))).agregate('total') #.aggregate(total=Sum('count', field="count*cost"))['total']
    var = []
    #{"list":[{"id":"2","count":1}]}
    kor = list()
    while x>=0:
        print("цикл: ", ids[x])
        try:
            i = ids[x]
            if len(i) > 0:
                t=models.Variaciya.objects.get(id=int(i))
                print(t.gallery)
                k = models.Korzina()
                k = t
                k.count=cts[x]
                k.summ=int(k.count) * int(t.tovar.cost)
                var.append(k)
                itog = itog + k.summ
                kor.append({'id':t.id, 'count': cts[x]})
            else:
                ids.pop(x)

        except ObjectDoesNotExist:
            print("Either the entry or blog doesn't exist.")
            ids.pop(x)
        x-=1

    print("VAR: ", var)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/api/korzina_get.html',
        {
            'title':'Корзина',
            'message':'бла бла бла',
            'kor': json.dumps(kor),
            'korz': var,
            'itog': itog,
            'year':year(),
        }
    )