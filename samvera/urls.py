"""
Definition of urls for samvera.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms
from app.views import views, pages, adminka
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include


urlpatterns = [
    path('', views.home, name='home'),
    #path('viktoleon/', views.viktoleon, name='viktoleon'),
    path('kabinet/', views.kabinet, name='kabinet'),
    path('about/<str:page>', pages.about, name='about'),
    path('contact/<str:page>', pages.about, name='contact'),
    path('thing/<int:id>', views.thing, name='thing'),
    path('post/<str:code>/', views.post, name='post'),
    path('info/<str:page>', pages.info, name='info'),
    path('catalog/', pages.catalog, name='catalog'),
    path('catalog/<str:page>', pages.catalog),
    path('korzina/', views.korzina, name='korzina'),
    path('korzinaget/', views.korzina_get, name='korzinaget'),
    path('getthingcolors/<int:tovar>/<str:size>/', views.getthingcolors, name='getthingcolors'),
    path('getthingphtotoss/<int:variaciya>/', views.getthingphtotoss, name='getthigetthingphtotossngcolors'),
    path('order/', views.new_order, name='new_order'),
    path('orderget/', views.get_order, name='get_order'),
    path('login/', LoginView.as_view(template_name = 'app/account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='log_out'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('adminka/', adminka.main),
    path('adminka/thing/edit/<int:id>/', adminka.thing_edit, name='thing_edit'),
    path('adminka/thing/delete/<int:id>/', adminka.thing_delete, name='thing_delete'),
    path('adminka/variaciya/edit/<int:id>/', adminka.variaciya_edit, name='variaciya_edit'),
    path('adminka/variaciya/delete/<int:id>/', adminka.variaciya_delete, name='variaciya_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


