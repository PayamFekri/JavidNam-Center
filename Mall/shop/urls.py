from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),  # صفحه اصلی جدید
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/remove-ajax/', views.cart_remove_ajax, name='cart_remove_ajax'),
    path('checkout/', views.order_create, name='order_create'),

]