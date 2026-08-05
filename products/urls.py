from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('products/', product_list, name='products'),

    path(
        'product/<int:product_id>/',
        product_detail,
        name='product_detail'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart_page,
        name='cart'
    ),

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    path(
        'my-orders/',
        my_orders,
        name='my_orders'
    ),

    path(
        'remove-from-cart/<int:cart_id>/',
        remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase-quantity/<int:cart_id>/',
        increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease-quantity/<int:cart_id>/',
        decrease_quantity,
        name='decrease_quantity'
    ),

    
    path(
    'account/',
    account_page,
    name='account'
),
path(
    'dashboard/',
    dashboard,
    name='dashboard'
),
path(
    'wishlist/',
    wishlist_page,
    name='wishlist'
),

path(
    'add-to-wishlist/<int:product_id>/',
    add_to_wishlist,
    name='add_to_wishlist'
),
path("contact/", contact, name="contact"),
path(
    "about/",
    about,
    name="about"
),
path("account/", account, name="account"),  

path(
    "order/<int:order_id>/",
    order_details,
    name="order_details"
),



]