"""pricetracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('urun-listem/', views.manage, name='manage'),
    path('disable-notification/<int:id>/', views.disable_notification, name='cancel-notification'),
    path('active-notification/<int:id>/', views.active_notification, name='open-notification'),
    path('delete-product/<int:id>', views.delete_product, name='delete'),
    path('telegram-settings/', views.install_telegram, name='telegram'),
    url('', include('social_django.urls', namespace='social')),
    path('telegram-key', views.telegram_code_request, name="key-request")
]
