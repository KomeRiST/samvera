from django.contrib import admin
from django import forms
from app.models import *
from app.models import ColorField
#from nested_inline.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

admin.site.register(StatusOrder)
admin.site.register(PotentialClient)
admin.site.register(Orders)
admin.site.register(OrderTovary)
admin.site.register(Tovar)
admin.site.register(OrderTovaryVariaciya)
#admin.site.register(Variaciya)


class GallAdmin(admin.ModelAdmin):
    model = Gallery
    list_display = ['image_img',]

admin.site.register(Gallery, GallAdmin)

class ImageInline(admin.TabularInline):
    model = Gallery
    extra = 1


#@admin.register(Variaciya)
class VariaciyaAdm(admin.ModelAdmin):
    inlines = [ImageInline,]
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

admin.site.register(Variaciya, VariaciyaAdm)

#class VarInline(NestedStackedInline):
#    model = OrderTovaryVariaciya
#    extra = 1
#    fk_name = 'ordertovar'

#class OrderTovaryInline(NestedStackedInline):
#    model = OrderTovary
#    fk_name = "order"
#    extra = 1
#    inlines = [VarInline]


#class OrdersAdm(NestedModelAdmin):
#    model = Orders
#    read_only = ['namber']
#    inlines = [OrderTovaryInline]
    
#admin.site.register(Orders, OrdersAdm)


#class LevelThreeInline(NestedStackedInline):
#    model = LevelThree
#    extra = 1
#    fk_name = 'level'


#class LevelTwoInline(NestedStackedInline):
#    model = Gallery
#    extra = 1
#    fk_name = 'product'


#class LevelOneInline(NestedStackedInline):
#    model = Variaciya
#    extra = 1
#    fk_name = 'tovar'
#    inlines = [LevelTwoInline]


#class TopLevelAdmin(NestedModelAdmin):
#    model = Tovar
#    inlines = [LevelOneInline]


#admin.site.register(Tovar, TopLevelAdmin)