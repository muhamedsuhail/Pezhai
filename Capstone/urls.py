from django.urls import path,include
from . import views
# from django.conf.urls.defaults import *


urlpatterns = [
    path('',views.index, name="index"),
    path('register',views.register_view, name="register"),
    path('login',views.login_view, name="login"),
    path('logout',views.logout_view, name="logout"),
    path('product/<int:product_id>',views.product_page, name='p_page'),
    path('checkout/',views.checkout,name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('<str:tag>',views.index, name="index"),
]