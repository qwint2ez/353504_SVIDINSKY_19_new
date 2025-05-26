from django.urls import path
from . import views
from .views import (
    HomeView, MenuView, PizzaDetailView, PizzaCreateView, 
    PizzaUpdateView, PizzaDeleteView, OrderCreateView, 
    ReviewCreateView, OrdersListView, MyOrdersView,
    CouriersListView
)
from django.contrib.auth import views as auth_views

app_name = 'pizza'

urlpatterns = [
    # Base URLs
    path('', HomeView.as_view(), name='home'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('search/', views.MenuView.as_view(), name='pizza_search'),
    path('about/', views.about_view, name='about'),
    path('news/', views.ArticleListView.as_view(), name='news'),
    path('faq/', views.faq_view, name='faq'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('jobs/', views.jobs_view, name='jobs'),
    
    # Reviews URLs
    path('reviews/', views.reviews_list, name='reviews_list'),
    path('reviews/new/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/success/', views.review_success, name='review_success'),
    
    # Order URLs
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    path('order/new/', OrderCreateView.as_view(), name='order_create'),
    path('order/complete/', views.order_complete, name='order_complete'),
    
    # Pizza URLs
    path('pizza/<int:pk>/', PizzaDetailView.as_view(), name='pizza_detail'),
    path('pizza/create/', PizzaCreateView.as_view(), name='pizza_create'),
    path('pizza/<int:pk>/edit/', PizzaUpdateView.as_view(), name='pizza_update'),
    path('pizza/<int:pk>/delete/', PizzaDeleteView.as_view(), name='pizza_delete'),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='pizza/login.html',
        next_page='pizza:menu'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Additional URLs
    path('statistics/', views.statistics_view, name='statistics'),
    path('couriers/', CouriersListView.as_view(), name='couriers_list'),
    path('promotions/', views.promotions_view, name='promotions'),
    path('promo/apply/', views.apply_promo, name='apply_promo'),
    
    # Order management URLs
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('order/<int:pk>/assign-courier/', views.assign_courier, name='assign_courier'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
