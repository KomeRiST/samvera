from .models import Category, Collection

def categories(request):
    return {'categories': Category.objects.all()}

def collections(request):
    return {'collections': Collection.objects.all()}   