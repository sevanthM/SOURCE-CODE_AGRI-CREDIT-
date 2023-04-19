from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings 


from .views import *
urlpatterns = [
path('', homeview.as_view(),name="home"),
path('sell-produce', sellproduce.as_view(),name="sell"),
path('profile', profileview.as_view(),name="profile"),

path('register', registerview.as_view(),name="register"),
path('login',loginview.as_view(),name="login"),
path('logout',logout_request,name="logout"),


path('fertilizer-aggregators', aggrefertileview.as_view(),name="aggrefert"),
path('fertilizer-farmers', farmfertileview.as_view(),name="farmfert"),


path('machinary-aggregators',aggremachinaryview.as_view(),name="aggrmachine"),
path('machinary-farmers',farmmachinaryview.as_view(),name="famrmachine"),


path('pesticides-aggragators',aggrepestiview.as_view(),name="aggrpesti"),
path('pesticides-farmers',farmpestiview.as_view(),name="farmpesti"),


path('seeds-aggragators',aggreseedview.as_view(),name="aggrseed"),
path('seeds-farmers',farmseedview.as_view(),name="farmseed"),


path('fertilizer/<str:str>',detailedfertview.as_view(),name="detailfert"),
path('machinary/<str:str>',detailedmachview.as_view(),name="detailmach"),
path('pesticides/<str:str>',detailedpestview.as_view(),name="detailpest"),
path('seeds/<str:str>',detailedseedview.as_view(),name="detailseed"),
path('my-orders',ordersview.as_view(),name="orders"),
path('my-products',productsview.as_view(),name="products"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
