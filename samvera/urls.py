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
    path('contact/', views.contact, name='contact'),
    path('things/', views.things, name='things'),
    path('post/<str:code>/', views.post, name='post'),
    path('about/<str:page>', views.about, name='about'),
    path('info/<str:page>', views.info, name='info'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:page>', views.catalog),
    path('korzina/', views.korzina, name='korzina'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


