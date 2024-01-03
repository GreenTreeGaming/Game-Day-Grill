from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('store/', views.store, name='store'),
    path('appetizers/', views.appetizers, name='appetizers'),
    path('maincourses/', views.maincourses, name='maincourses'),
    path('sides/', views.sides, name='sides'),
    path('desserts/', views.desserts, name='desserts'),
    path('extras/', views.extras, name='extras'),

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('process_reservation/', views.processReservation, name='process_reservation'),

    path('contact/', views.contact, name='contact'),
    path('reservation/', views.reservation, name='reservation'),

    path('events/', views.events, name='events'),
]