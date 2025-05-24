from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PizzaListView, PizzaDetailView, PizzaCreateView,
    PizzaUpdateView, PizzaDeleteView, OrderCreateView,
    ReviewCreateView, create_payment_intent
)
from . import views

app_name = 'pizza'

urlpatterns = [
    path('', PizzaListView.as_view(), name='pizza_list'),
    path('pizza/<int:pk>/', PizzaDetailView.as_view(), name='pizza_detail'),
    path('pizza/create/', PizzaCreateView.as_view(), name='pizza_create'),
    path('pizza/<int:pk>/update/', PizzaUpdateView.as_view(), name='pizza_update'),
    path('pizza/<int:pk>/delete/', PizzaDeleteView.as_view(), name='pizza_delete'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('login/', auth_views.LoginView.as_view(template_name='pizza/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create-payment-intent/', create_payment_intent, name='create_payment_intent'),
    path('order/complete/', views.order_complete, name='order_complete'),
]
