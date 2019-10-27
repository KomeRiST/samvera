from django.http import Http404, HttpRequest
from django.shortcuts import render
from app import models

ABOUT_PAGE = ("about", "contacts", "rabota-u-nas")
ABOUT_PAGE_DESCR = {
    "about":{
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
                "title": "Публичная оферта",
                "message": "Настоящий документ является публичной офертой (Далее – Оферта) ИП Соколовский Дмитрий Михайлович о продаже дистанционным способом товаров, представленных на официальном интернет-сайте Продавца https://www.samvera.ru",
                "message2": "Данная Оферта регламентируют предложение и продажу товаров на сайте https://www.samvera.ru"
            },
        "oplata":{
                "title": "Оплата",
                "message": ""
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
                "title": "Правила возврата и обмена",
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

def about(request, page):
    """Менеджер рендера страниц раздела ABOUT"""
    assert isinstance(request, HttpRequest)
    if page in ABOUT_PAGE:
        PAGE = f'app/about/{page}.html'
        DESC = ABOUT_PAGE_DESCR.get(page)
        #DESC["year"] = year()
        return render(
            request,
            PAGE,
            DESC
        )
    else:
        raise Http404

def info(request, page):
    """Менеджер рендера страниц раздела INFO"""
    
    print(f'\nPAGE:\n{page}\n')
    assert isinstance(request, HttpRequest)
    DESC = INFO_PAGE_DESCR.get(page)
    print(f'\nITEM FROM CONST:\n{DESC}\n')
    if DESC is not None:
        PAGE = f'app/info/{page}.html'
        #DESC["year"] = year()
        return render(
            request,
            PAGE,
            DESC
        )
    else:
        raise Http404

def catalog(request, page="catalog"):
    """Менеджер рендера страниц раздела CATALOG"""
    if not request.user.is_staff:
        th = models.Tovar.objects.filter(hidden=True)
    else:
        th = models.Tovar.objects.all()

    print(f'\nPAGE:\n{page}\n')
    assert isinstance(request, HttpRequest)
    DESC = CATALOG_PAGE_DESCR.get(page)
    print(f'\nITEM FROM CONST:\n{DESC}\n')
    if DESC is not None:
        PAGE = f'app/catalog/{page}.html'
        #DESC["year"] = year()
        DESC['things'] = th
        return render(
            request,
            PAGE,
            DESC
        )
    else:
        raise Http404
