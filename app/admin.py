from django.contrib import admin
from django import forms
from django.db import models
from app.models import *
# from app.models import ColorField
from orders.models import *
from fabricator.models import *
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
#admin.site.register(consignment)
admin.site.register(MtoM_VarsToCons)

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
    fields = ['tovar', 'article', ('color_text', 'color'), 'size', ('obmer', 'model'), 'kolvo', 'consignments']
    readonly_fields = ['kolvo', ]
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
    fields = ['tovar', ('color', 'color_text'), ('size', 'kolvo'), ('obmer', 'model')]
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
    readonly_fields = ['kolvo',]
    #list_display = []

class MtM_VariaciyaInline(nested_admin.nested.NestedTabularInline):
    # inlines = [ImageInline,]
    model = MtoM_VarsToCons
    save_on_top = True
    extra = 0
    # readonly_fields = ['nds_summ', 'total_not_nds', 'total_nds']
    # raw_id_fields = ['variacii',]


    # def nds_summ(self, obj):
    #     return (obj.nds * obj.cost / 100) * obj.kolvo

    # def total_not_nds(self, obj):
    #     return obj.cost * obj.kolvo

    # def total_nds(self, obj):
    #     return (obj.nds * obj.cost / 100 * obj.kolvo) + (obj.cost * obj.kolvo)

    class Media:
        js = [ '/static/admin/js/consignment.js', ]
        

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

class ConsignmentInline(nested_admin.nested.NestedStackedInline):
    inlines = [MtM_VariaciyaInline,]
    model = consignment
    exstra = 0
    readonly_fields = ['data_create', 'data_change',]
    fields = [('number', 'data_doc'), 'responsible', ('data_create', 'data_change')]

@admin.register(fabricator)
class FabricatorAdmin(nested_admin.nested.NestedModelAdmin):
    inlines = [ConsignmentInline,]
    fields=['title', 'slug', 'address', 'contacts', 'data_create', 'data_change']
    readonly_fields = ['data_create', 'data_change',]
    prepopulated_fields={'slug':('title',)}
    
@admin.register(consignment)
class ConsignmentAdmin(nested_admin.nested.NestedModelAdmin):
    inlines = [MtM_VariaciyaInline,]
    list_display = ['number', 'fabricator', 'closed', 'data_doc', 'count_sku', 'count_variacii', 'summ_itog']
    fields=[('fabricator', 'number'), ('data_doc', 'responsible'), ('closed', 'data_create', 'data_change')]
    readonly_fields = ['data_create', 'data_change',]

    def count_sku(self, obj):
        return MtoM_VarsToCons.objects.filter(consignments=obj).count()
    count_sku.short_description = 'Кол-во позиций'

    def count_variacii(self, obj):
        from django.db.models import Sum
        return MtoM_VarsToCons.objects.filter(consignments=obj).aggregate(count_var=Sum('kolvo'))
    count_variacii.short_description = 'Всего штук'

    def summ_itog(self, obj):
        from django.db.models import Sum
        return MtoM_VarsToCons.objects.filter(consignments=obj).aggregate(summ_itog=Sum('total_nds'))
    summ_itog.short_description = 'Сумма'