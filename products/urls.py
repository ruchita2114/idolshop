from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),

    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/decrease/<int:product_id>/", views.cart_decrease, name="cart_decrease"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),

    path("checkout/", views.checkout, name="checkout"),

    path("<slug:slug>/", views.product_detail, name="product_detail"),
]