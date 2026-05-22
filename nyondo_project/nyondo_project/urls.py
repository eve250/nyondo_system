"""
URL configuration for nyondo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from nyondo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.viewstock, name='viewstock'),
    path('creditscheme/',views.creditscheme, name='creditscheme'),
    path('viewsales/',views.viewsales, name='viewsales'),
    path('addsale/',views.addsale, name='addsale'),
    path('receipt/<int:receipt_number>/', views.receipt, name='receipt'),
    path('categories/',views.categories, name='categories'),
    path('products/',views.products, name='products'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutuser, name='logout'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
]
