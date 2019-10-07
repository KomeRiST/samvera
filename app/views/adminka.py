# Вьюшка для работы с админкой

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from app import models, forms

def main(request):
    assert isinstance(request, HttpRequest)

    if (request.user is not None) and (request.user.is_staff):
        return render(
            request,
            'app/adminka/adm_main.html',
            {
                'title':'Администрирование',
                'things': models.Tovar.objects.all()[:10],
                'orders': models.Orders.objects.filter(status_id__gt=1)[:10]
            }
        )
    else:
        return Http404(request)

def thing_edit(request, id):
    assert isinstance(request, HttpRequest)
    try:
        thing = get_object_or_404(models.Tovar, id=id)
 
        if request.method == "POST":
            form = forms.ThingEditForm(request.POST, instance=thing)
            if form.is_valid():
                thing = form.save(commit=False)
                # Добавить дату последнего редактирования.
                thing.save()
            return HttpResponseRedirect("/")
        else:
            form = forms.ThingEditForm(instance=thing)
            return render(request, "app/adminka/thing/edit.html", {"thing": thing, "form": form, "title": "Редактирование товара"})
    except models.Tovar.DoesNotExist:
        return HttpResponseNotFound("<h2>Запрошенный элемент не найден!</h2>")
    
def thing_delete(request, id):
    assert isinstance(request, HttpRequest)
    try:
        thing = models.Tovar.objects.get(id=id)
 
        if request.method == "POST":
            thing.title = request.POST.get("title")
            thing.descr = request.POST.get("descr")
            thing.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"person": person})
    except models.Tovar.DoesNotExist:
        return HttpResponseNotFound("<h2>Запрошенный элемент не найден!</h2>")

    
def variaciya_edit(request, id):
    from django.forms import formset_factory
    from django.forms.models import modelformset_factory

    assert isinstance(request, HttpRequest)
    try:
        variaciya = get_object_or_404(models.Variaciya, id=id)
 
        if request.method == "POST":
            form = forms.VariaciyaEditForm(request.POST, instance=variaciya)
            if form.is_valid():
                variaciya = form.save(commit=False)
                # Добавить дату последнего редактирования.
                variaciya.save()
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            form = forms.VariaciyaEditForm(instance=variaciya)
            photosSet = formset_factory(forms.VarPhotoForm, can_delete=True)
            g=variaciya.gallery.all().values('image')
            photos = photosSet(initial=g)
            return render(request, "app/adminka/thing/edit.html", {"variaciya": variaciya, "form": form, "photos": photos, "title": "Редактирование вариации товара", 'g': g})
    except models.Variaciya.DoesNotExist:
        return HttpResponseNotFound("<h2>Запрошенный элемент не найден!</h2>")
    
def variaciya_delete(request, id):
    assert isinstance(request, HttpRequest)
    try:
        variaciya = models.Variaciya.objects.get(id=id)
 
        if request.method == "POST":
            variaciya.title = request.POST.get("title")
            variaciya.descr = request.POST.get("descr")
            variaciya.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"variaciya": variaciya})
    except models.Tovar.DoesNotExist:
        return HttpResponseNotFound("<h2>Запрошенный элемент не найден!</h2>")
  