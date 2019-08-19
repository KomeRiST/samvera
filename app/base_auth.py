import json
from http.client import HTTPSConnection, HTTPException
from base64 import b64encode

basedir = '/api/remap/1.1'
ms = '/https://online.moysklad.ru'


def baseAuth(s1):
    theurl = 'online.moysklad.ru'
    username = 'komerist1993-93@mail.ru'
    password = 'KrMkh999z9n'
    # a great password

    #This sets up the https connection
    c = HTTPSConnection(theurl)
    #we need to base 64 encode it
    #and then decode it to acsii as python 3 stores it as a byte string
    userAndPass = b64encode(bytes(f'{username}:{password}', "utf-8")).decode("ascii")

    headers = { 'Authorization' : 'Basic %s' % userAndPass }
    #then connect
    print(f'\n baseAuth \n{basedir + s1}\n')
    c.request('GET', basedir + s1, headers=headers)
    #get the response back
    res = c.getresponse()
    print(f'return auth: {res.status};\n')
    # at this point you could check the status etc
    # this gets the page text
    #data = res.read()
    #print (data)
    r = json.loads(res.read())
    #c.close
    return r

def dpole_kollection():
    #/entity/product/metadata
    b=baseAuth('/entity/product/metadata')
    print(f'\n dpole_kollection \n{b}\n')
    if "errors" in b:
        return -1, b["errors"][0]["error"]
    href = b['attributes'][0]['customEntityMeta']['href']
    href = href.split('/')
    l=href.__len__()
    r = href[l - 1]
    return 0, r

sklad_href = {
    "получить": {
        'группы_товаров':'/entity/productfolder',
        'товары':'/entity/product',
        'коллекции':f'/entity/customentity/',
        #'коллекции':f'/entity/product?filter={ms}{basedir}/entity/product/metadata/attributes/{dpole_kollection()}={entity_href()}/{kollection_id()}',}
    }
    }

#https://online.moysklad.ru/api/remap/1.1/entity/product/metadata
    #возвращает список дополнительных полей сущности (товара)

#https://online.moysklad.ru/api/remap/1.1/entity/companysettings/metadata
    #Получает список справочников
        #customEntities - массив
        #customEntities.name - название справочника
        #customEntities.entityMeta.href=https://online.moysklad.ru/api/remap/1.1/entity/customentity/6c490ed1-a573-11e9-912f-f3d4000d4674
        #- на конце ссылки ID справочника

#https://online.moysklad.ru/api/remap/1.1/entity/customentity/<customentity_id>
    #Получает элементы пользовательского справочника
        #<customentity_id> - ID пользовательского справочника
        #(6c490ed1-a573-11e9-912f-f3d4000d4674)
    #rows.name - название элемента справочника
    #rows.id - ID элемента справочника (38876933-a607-11e9-9ff4-34e8000f4dc4)


#https://online.moysklad.ru/api/remap/1.1/entity/product/ filter=<ссылка на
#доп.поле>=<ссылка на сущность>
    #<ссылка на доп.поле> - для фильтрации
        #http://online.moysklad.ru/api/remap/1.1/entity/<type>/metadata/attributes/<id>
        #<type> - например "product", "productFolder" и т.д.
        #<id>
    #<ссылка на сущность>
        #http://online.moysklad.ru/api/remap/1.1/entity/<type>/<id>
        #<type> - например "product", "productFolder" и т.д.
        #<id>

#Получаем список пользовательских справочников
    #Находим нужный справчник
    #берем его ИД

    #Запрос ниже получает товары с фильтром по коллекции
    #https://online.moysklad.ru/api/remap/1.1/entity/product?filter=https://online.moysklad.ru/api/remap/1.1/entity/product/metadata/attributes/793f134e-a573-11e9-9ff4-34e8000d8e09=https://online.moysklad.ru/api/remap/1.1/entity/customentity/6c490ed1-a573-11e9-912f-f3d4000d4674/b2f42622-a573-11e9-9ff4-34e8000d9471



def zapros(s1, s2):
    theurl = 'online.moysklad.ru'
    h = basedir + sklad_href[s1][s2]
    print(f'\nzapros\n{h}\n')
    if s2=='коллекции':
        coderes, res = dpole_kollection()
        if coderes == 0:
            h=h+dp
        elif coderes == -1:
            return None
    c = HTTPSConnection(theurl)
    username = 'komerist1993-93@mail.ru'
    password = 'KrMkh999z9n'
    userAndPass = b64encode(bytes(f'{username}:{password}', "utf-8")).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' % userAndPass,
              'Lognex-Pretty-Print-JSON': 'true'}
    try:
        print(f'\nzapros\n{h}\n')
        c.request('GET', h, headers=headers)
        res = c.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)
        #from pprint import pprint
        print(f'\nzapros__response\n{data}\n')
        #c.close
        return data
    except HTTPException as e:
        print(f'Всё плохо: {e}')
        #c.close
        return None
        pass

#zapros("получить","группы_товаров")
#zapros("получить","коллекции") #https://online.moysklad.ru/api/remap/1.1/entity/customentity/6c490ed1-a573-11e9-912f-f3d4000d4674
#baseAuth()