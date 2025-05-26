from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    HomeView, MenuView,
    PizzaDetailView, PizzaCreateView, PizzaUpdateView, PizzaDeleteView,
    OrderCreateView, ReviewCreateView, OrdersListView
)

app_name = 'pizza'

urlpatterns = [
    # Базовые URL
    path('', views.HomeView.as_view(), name='home'),  # Используем HomeView как главную
    path('menu/', views.MenuView.as_view(), name='menu'),

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
    path('login/', auth_views.LoginView.as_view(
        template_name='pizza/login.html',
        next_page='pizza:pizza_list'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # API URLs
    re_path(r'^api/payment/create/$', views.create_payment_intent, name='create_payment_intent'),

    # Статистика
    path('statistics/', views.statistics_view, name='statistics'),

    # URL для успешного создания пиццы
    path('pizza/create/success/', views.pizza_create_success, name='pizza_create_success'),

    # URLs для промоакций
    path('promotions/', views.promotions_view, name='promotions'),
    path('promotions/apply/', views.apply_promo, name='apply_promo'),

    # Orders management
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/my/', views.MyOrdersView.as_view(), name='my_orders'),
    path('couriers/', views.CouriersListView.as_view(), name='couriers_list'),
    path('promos/', views.promo_list, name='promo_list'),
]
