"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from app import forms, models, base_auth
from django.core.mail import send_mail
from django.db.models import Sum
from django.forms import formset_factory
import json
from django.core import serializers

ABOUT_PAGE = ("brend", "contacts", "rabota-u-nas")
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
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def things(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/thing.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

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
    
        return render(
            request,
            p,
            {
                'title':'About',
                'message':'Your application description page.',
                'year':datetime.now().year,
            }
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

def dictfetchall(cursor):
    columns = [col[0] for col in cursor]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def korzina_get(request):
    """Renders the contact page."""
    itog = 16000
    arr=[]
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
    c=len(cts)
    x=0
    itog=0
    msg = []
    #korz = models.Variaciya.objects.filter(id__in=map(float, arr.split(',')))
    #tovary = models.Variaciya.objects.filter(id__in=map(int, arr.split(','))).agregate('total') #.aggregate(total=Sum('count', field="count*cost"))['total']
    var = []

    while x<c:
        print("цикл: ", ids[x])
        t=models.Variaciya.objects.get(id=int(ids[x]))
        #msg.append(f'{t.size} | {t.color}')
        print(t.gallery)
        #t.total=t.tovar.cost*cts[x]
        #k = models.Korzina()
        k = json.dumps(t)
        print ("t = ", [k, ])
        k.count=cts[x]
        k.summ=int(k.count) * int(t.tovar.cost)
        var.append(k)
        itog = itog + k.summ
        x+=1
    print("VAR: ", var)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/api/korzina_get.html',
        {
            'title':'Корзина',
            'message':'бла бла бла',
            'korz': var,
            'itog': itog,
            'year':datetime.now().year,
        }
    )