from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name='shopHome'),
    path('about',views.about, name='aboutUs'),
    path('contact',views.contact, name='contactUs'),
    path('tracker',views.tracker, name='tracker'),
    path('productview/<int:myid>/',views.prodView, name='prodView'),
    path('checkout',views.checkout, name='checkout'),
]