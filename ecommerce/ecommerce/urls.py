
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from .import views

urlpatterns = [
    #for eror page
    path('404', views.Error404, name='404'),

    #for account url
    path('account/register', views.REGISTRATER, name='handle_register'),
    path('account/login', views.LOGIN, name='handle_login'),
    path('account/profile', views.PROFILE, name='profile'),
    path('account/profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('logout', views.LOGOUT, name='logout'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),


    path('base/', views.BASE, name='base'),

    path('', views.HOME, name='home'),
    path('about', views.ABOUT, name='about'),
    path('contact', views.CONTACT, name='contact'),
    path('product', views.PRODUCT, name='product'),

    path('product/filter-data', views.filter_data, name="filter-data"),

    path('product/<slug:slug>', views.PRODUCT_DETAIL, name='product_detail'),

    path('product_search', views.SEARCH, name='product_search'),

    path('Main-Category', views.MAIN_CATEGORY, name='product_main'),


    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart/checkout/', views.CheckOut, name='checkout'),
    path('PlaceOrder', views.PLACE_ORDER, name='placeorder')






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
