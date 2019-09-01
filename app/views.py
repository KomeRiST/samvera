"""
Definition of views.
"""
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from app import forms, models, base_auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Sum
from django.forms import formset_factory
import json
from django.core import serializers
from django.template.loader import render_to_string

ABOUT_PAGE = ("brend", "contacts", "rabota-u-nas")
ABOUT_PAGE_DESCR = {
    "brend":{
        "title":"О нас",
        "message":""
    },
    "contacts":{
        "title":"Контакты",
        "message":"Ниже представлены контакты для связи с нами"
    },
    "rabota-u-nas":{
        "title":"Вакансии",
        "message":""
    }
}
INFO_PAGE = ("dostavka", "faq", "idei", "oferta", "oplata", "politika-konfidencialnosti", "preorder", "rukovodstvo-po-pokupke", "samovyvoz", "vozvrattovar")
INFO_PAGE_DESCR = {
        "dostavka":{
                "title": "Доставка",
                "message": "Подробности и условия доставки"
            },
        "faq":{
                "title": "Частые вопросы",
                "message": "Здесь мы собрали для Вас ответы на самые частозадоваемые вопросы."
            },
        "idei":{
                "title": "Ваши идеи",
                "message": "Делитесь своими идеями!"
            },
        "oferta":{
                "title": "Оферта",
                "message": ""
            },
        "oplata":{
                "title": "Оплата",
                "message": "Ниже изложена исчерпывающая информация об оплате заказа"
            },
        "politika-konfidencialnosti":{
                "title": "Политика конфиденциальности",
                "message": ""
            },
        "preorder":{
                "title": "Предоплата",
                "message": ""
            },
        "rukovodstvo-po-pokupke":{
                "title": "Руководство по покупке",
                "message": ""
            },
        "samovyvoz":{
                "title": "Самовывоз",
                "message": ""
            },
        "vozvrattovar":{
                "title": "Возврат товара",
                "message": ""
            }
    }

CATALOG_PAGE_DESCR = {
        "new":{
                "title": "Новинки!",
                "message": "Для тех кто в тренде"
            },
        "sale":{
                "title": "Скидки",
                "message": "Успейте приобрести по низкой цене!"
            },
        "catalog":{
                "title": "LOOKBOOK",
                "message": "Найдите для себя что-то новое"
            },
    }


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
            #'tovarfolder': tovarfolder,
            #'kollections': kollections,
            'year':datetime.now().year,
            #'Form_PotentialClient': forms.Form_PotentialClient,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Связаться с нами Вы можете по контактам ниже',
            'year':datetime.now().year,
        }
    )

def thing(request, id):
    """Renders the contact page."""
    t = get_object_or_404(models.Tovar, pk=id)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/thing.html',
        {
            'title':t.title,
            'thing': t,
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def kabinet(request):
    """Renders the contact page."""
    if request.user.is_authenticated:
        title = "Личный кабинет"
        message = "Посмотрите исторю своих покупок, а также статус текущих заказов."
        orders = models.Orders.objects.filter(client=request.user.id)
        page = 'app/lk.html'
        assert isinstance(request, HttpRequest)
        return render(
            request,
            page,
            {
                'title':title,
                'message':message,
                'orders':orders,
                'year':datetime.now().year,
            }
        )
    else:
        from django.contrib.auth.forms import AuthenticationForm
        title="Вход на сайт"
        message="Введите свои данные для входа на сайт"
        page = 'app/login.html'
        orders=None
        assert isinstance(request, HttpRequest)
        return render(
            request,
            page,
            {
                'title':title,
                'message':message,
                'form':AuthenticationForm,
                'year':datetime.now().year,
            }
        )

def getthingcolors(request, tovar, size):
    """Renders the contact page."""
    t = get_object_or_404(models.Tovar, pk=tovar)
    print("tovar = ", t)
    r = t.variacii.filter(size=size, kolvo__gt=0)
    print("FILTER SIZE = ", r)
    st = ""
    for v in r:
        st = st + v.colortile_korz()
    assert isinstance(request, HttpRequest)
    return HttpResponse(st)

def getthingphtotoss(request, variaciya):
    """Renders the contact page."""
    v = get_object_or_404(models.Variaciya, pk=variaciya)
    print("variaciya = ", v)
    r = v.gallery.all()
    st = ""
    for i in r:
        st = st + f'<div class="carousel-cell" ><img src="/media/{i.image}" alt=""/></div>'
    res={}
    res['img']=st
    res['id']=v.id
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

def about(request, page):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if page in ABOUT_PAGE:
        p = f'app/about/{page}.html'
        b = ABOUT_PAGE_DESCR.get(page)
        b["year"] = datetime.now().year
        return render(
            request,
            p,
            b
        )
    else:
        raise Http404

def info(request, page):
    """Renders the about page."""
    
    print(f'\nPAGE:\n{page}\n')
    assert isinstance(request, HttpRequest)
    b = INFO_PAGE_DESCR.get(page)
    print(f'\nITEM FROM CONST:\n{b}\n')
    if b is not None:
        p = f'app/info/{page}.html'
        b["year"] = datetime.now().year
        return render(
            request,
            p,
            b
        )
    else:
        raise Http404

def catalog(request, page="catalog"):
    """Renders the about page."""
    
    th = models.Tovar.objects.all()

    print(f'\nPAGE:\n{page}\n')
    assert isinstance(request, HttpRequest)
    b = CATALOG_PAGE_DESCR.get(page)
    print(f'\nITEM FROM CONST:\n{b}\n')
    if b is not None:
        p = f'app/catalog/{page}.html'
        b["year"] = datetime.now().year
        b['things'] = th
        return render(
            request,
            p,
            b
        )
    else:
        raise Http404

def korzina(request):
    """Renders the contact page."""
    if request.POST:
        pass
    else:
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/korzina.html',
            {
                'title':'Корзина',
                'message':'бла бла бла',
                'year':datetime.now().year,
            }
        )

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
                'year':datetime.now().year,
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
                'year':datetime.now().year,
            }
        )
    
def get_order(request):
    """ Рендер страницы подтверждения заказа """
    if request.method == 'POST':
        try:
            # Проверить пользователя по его телефону
            user = User.objects.get(username = request.POST['phone'], email = request.POST['email'])
        except ObjectDoesNotExist:
            # Создать пользователя
            password =  User.objects.make_random_password()
            user = User.objects.create_user(request.POST['phone'], request.POST['email'], password)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
        # Создать заказ
        order = models.Orders()
        order.client = user
        order.status = models.StatusOrder.objects.get(id=2) # Принят в обработку
        order.save()
        korz = request.POST['korzina']

        # korz = {"l": [{"id": 1, "count": "1"}, {"id": 2, "count": "2"}]}
        korz = json.loads(korz)
        for item in korz['l']:
            pass
            #print("цикл: ", ids[x])
            try:
                if item['id'] != '':
                    t=models.Variaciya.objects.get(id=int(item['id']))


                    ordertovarvariaciya = models.OrderTovaryVariaciya()

                    ordertovar, created = models.OrderTovary.objects.get_or_create(order=order, tovar=t.tovar)
                    ordertovarvariaciya.ordertovar = ordertovar

                    ordertovarvariaciya.variaciya = t
                    ordertovarvariaciya.count = int(item['count'])
                    ordertovarvariaciya.save()

                else:
                    ids.pop(x)

            except ObjectDoesNotExist:
                print("Either the entry or blog doesn't exist.")
                ids.pop(x)

        # Отправить на почту оператора состав заказа с реквизитами клиента для связи с ним и пдт заказа. , 'viktoleon@bk.ru'
        html_message = render_to_string(
            'app/email-order_template.html',
            {
                'order': order,
            }
        )
        print("html_message = \n")
        print(html_message)
        send_mail("Новая заявка!!!", f"ФИО {user.last_name} {user.first_name}\n\
                Email {user.email}\n\
                Тел. {user.username}\n\
                \n\
                ", 'komerist1993-93@mail.ru', ['komerist1993-93@mail.ru'], html_message=html_message)

        # Отправить на почту клиенту уведомление о формировании заказа.
        
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/good_order.html',
            {
                'title':'Заказ принят на обработку',
                'message':'Спасибо за оформление заказа. С Вами скоро свяжутся.',
                'mess': html_message,
                'year':datetime.now().year,
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
                'year':datetime.now().year,
            }
        )


def korzina_get(request):
    """Renders the contact page."""
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
    kor = {}
    kor['l'] = list()
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
                kor['l'].append({'id':t.id, 'count': cts[x]})
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
            'year':datetime.now().year,
        }
    )