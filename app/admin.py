from django.contrib import admin
from django import forms
from django.db import models
from app.models import *
from app.models import ColorField
from orders.models import *
from django.utils.safestring import mark_safe
#from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
import nested_admin

admin.site.register(StatusOrder)
admin.site.register(PotentialClient)
#admin.site.register(Category)
#admin.site.register(OrderTovary)
#admin.site.register(OrderTovaryVariaciya)
#admin.site.register(Variaciya)

# class OrderVarsInline(admin.TabularInline):
#     model = OrderTovaryVariaciya
#     fields = ['variaciya', 'count']

class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    # inlines = [OrderVarsInline,]
    #fields = ['variaciya', 'count']
    fields = ['tovar',]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemsInline,]
    fields = ['client', 'status', 'namber', 'date_create']
    readonly_fields = ['date_create', ]
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
    extra = 1
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
    fields = [('color_text', 'color'), ('size', 'kolvo')]
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
    #readonly_fields = ['image_img']
    #list_display = []


@admin.register(Tovar)
class TovarAdm(nested_admin.nested.NestedModelAdmin):
    inlines = [VariaciyaInline,]
    list_display = ['title', 'slug', 'count_var', 'sebestoimost', 'cost', 'data_create', 'hidden']
    fields = ['kod', ('title', 'category'),('slug', 'hidden', 'data_create'),('descr', 'uhod'), ('sebestoimost', 'cost')]
    readonly_fields = ['kod', 'data_create', 'count_var']
    prepopulated_fields = {'slug': ('title',)}

#@admin.register(Category)
#class CategoryAdmin(admin.ModelAdmin):
