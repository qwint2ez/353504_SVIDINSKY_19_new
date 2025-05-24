from django.urls import path
from .views import (
    PizzaListView, PizzaDetailView, PizzaCreateView,
    PizzaUpdateView, PizzaDeleteView, OrderCreateView,
    ReviewCreateView
)

app_name = 'pizza'

urlpatterns = [
    path('', PizzaListView.as_view(), name='pizza_list'),
    path('pizza/<int:pk>/', PizzaDetailView.as_view(), name='pizza_detail'),
    path('pizza/create/', PizzaCreateView.as_view(), name='pizza_create'),
    path('pizza/<int:pk>/update/', PizzaUpdateView.as_view(), name='pizza_update'),
    path('pizza/<int:pk>/delete/', PizzaDeleteView.as_view(), name='pizza_delete'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('review/create/', ReviewCreateView.as_view(), name='review_create'),
]
