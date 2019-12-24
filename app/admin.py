from django.contrib import admin
from django import forms
from django.db import models
from app.models import *
# from app.models import ColorField
from orders.models import *
from django.utils.safestring import mark_safe
#from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
import nested_admin

admin.site.register(StatusOrder)
admin.site.register(PotentialClient)
#admin.site.register(Category)
# admin.site.register(Order)
admin.site.register(OrderItem)
#admin.site.register(OrderTovaryVariaciya)
#admin.site.register(Variaciya)

# class OrderVarsInline(admin.TabularInline):
#     model = OrderTovaryVariaciya
#     fields = ['variaciya', 'count']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    fields=['title', 'slug']
    prepopulated_fields={'slug':('title',)}

class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    fields = ['variaciya', 'cost', 'count']
    # readonly_fields = ['variaciya', 'cost', 'count' ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemsInline,]
    extrta = 0
    fields = ['client', 'status', 'addres', 'date_create', 'date_update']
    readonly_fields = ['date_create', 'date_update' ]
    # list_editable = ['status', ]

@admin.register(Gallery)
class GallAdmin(admin.ModelAdmin):
    model = Gallery
    list_display = ['image_img', 'product', 'image']
    #image_fields = ['image', ]
    fields = ['product', 'image_img', 'image']
    readonly_fields = ['image_img', 'product']


class ImageInline(nested_admin.nested.NestedTabularInline):
    model = Gallery
    extra = 0
    fields = ['image_img', 'image']
    readonly_fields = ['image_img']



@admin.register(Variaciya)
class VariaciyaAdm(nested_admin.nested.NestedModelAdmin):
    inlines = [ImageInline,]
    list_display = ['random_image', 'tovar', 'article', 'color', 'color_text', 'size', 'obmer', 'model', 'kolvo']
    fields = ['tovar', 'article', ('color_text', 'color'), 'size', ('obmer', 'model'), 'kolvo']
    readonly_fields = []
    formfield_overrides = {
        ColorField: {
            'widget': forms.TextInput(
                attrs={
                    'type': 'color',
                    'style': 'height: 25px; width: 100px'
                    }
                )
            }
        }

class VariaciyaInline(nested_admin.nested.NestedStackedInline):
    inlines = [ImageInline,]
    model = Variaciya
    save_on_top = True
    extra = 0
    fields = [('color', 'color_text'), ('size', 'kolvo'), ('obmer', 'model')]
    formfield_overrides = {
        ColorField: {
            'widget': forms.TextInput(
                attrs={
                    'type': 'color',
                    'style': 'height: 25px; width: 25px; border-radius: 50%;'
                    }
                )
            }
        }
    #readonly_fields = ['image_img']
    #list_display = []


@admin.register(Tovar)
class TovarAdm(nested_admin.nested.NestedModelAdmin):
    inlines = [VariaciyaInline,]
    list_display = ['title', 'slug', 'collection', 'count_var', 'sebestoimost', 'cost', 'data_create', 'hidden']
    fields = ['kod', ('title', 'category', 'collection'),('slug', 'hidden', 'data_create'),('descr', 'uhod'), ('sebestoimost', 'cost')]
    readonly_fields = ['kod', 'data_create', 'count_var']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['sebestoimost', 'collection', 'cost', 'hidden']

#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):