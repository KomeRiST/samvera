"""
Definition of urls for samvera.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include


urlpatterns = [
    path('', views.home, name='home'),
    path('kabinet/', views.kabinet, name='kabinet'),
    path('about/<str:page>', views.about, name='about'),
    path('contact/<str:page>', views.about, name='contact'),
    path('thing/<int:id>', views.thing, name='thing'),
    path('post/<str:code>/', views.post, name='post'),
    path('info/<str:page>', views.info, name='info'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:page>', views.catalog),
    path('korzina/', views.korzina, name='korzina'),
    path('korzinaget/', views.korzina_get, name='korzinaget'),
    path('getthingcolors/<int:tovar>/<str:size>/', views.getthingcolors, name='getthingcolors'),
    path('getthingphtotoss/<int:variaciya>/', views.getthingphtotoss, name='getthigetthingphtotossngcolors'),
    path('order/', views.new_order, name='new_order'),
    path('orderget/', views.get_order, name='get_order'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/account/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='log_out'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


