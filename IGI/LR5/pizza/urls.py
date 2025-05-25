from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import (
    PizzaListView, PizzaDetailView, PizzaCreateView,
    PizzaUpdateView, PizzaDeleteView, OrderCreateView,
    ReviewCreateView, create_payment_intent
)
from . import views

app_name = 'pizza'

urlpatterns = [
    # Базовые URL
    path('', PizzaListView.as_view(), name='pizza_list'),
    
    # URLs с регулярными выражениями
    re_path(r'^pizza/(?P<pk>\d+)/$', PizzaDetailView.as_view(), name='pizza_detail'),
    re_path(r'^pizza/create/$', PizzaCreateView.as_view(), name='pizza_create'),
    re_path(r'^pizza/(?P<pk>\d+)/edit/$', PizzaUpdateView.as_view(), name='pizza_update'),
    re_path(r'^pizza/(?P<pk>\d+)/delete/$', PizzaDeleteView.as_view(), name='pizza_delete'),
    
    # URLs для заказов с regex
    re_path(r'^order/new/$', OrderCreateView.as_view(), name='order_create'),
    re_path(r'^order/complete/$', views.order_complete, name='order_complete'),
    re_path(r'^orders/(?P<year>\d{4})/(?P<month>\d{2})/$', views.orders_by_month, name='orders_by_month'),
    re_path(r'^orders/(?P<status>pending|preparing|delivering|completed)/$', views.orders_by_status, name='orders_by_status'),
    
    # URLs для отзывов
    path('review/new/', ReviewCreateView.as_view(), name='review_create'),
    path('review/success/', views.review_success, name='review_success'),
    path('reviews/', views.reviews_list, name='reviews_list'),
    
    # URLs для аутентификации
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='pizza/login.html'), name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    
    # API URLs
    re_path(r'^api/payment/create/$', create_payment_intent, name='create_payment_intent'),
    
    # Статистика
    path('statistics/', views.statistics_view, name='statistics'),
]
