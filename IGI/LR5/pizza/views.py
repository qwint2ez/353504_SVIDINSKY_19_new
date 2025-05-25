from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pizza, Order, Review, OrderItem, PizzaSize, PizzaPricing, Customer, PizzaCategory
from .forms import PizzaForm, OrderForm, ReviewForm, UserRegistrationForm
from .services import WeatherService, PaymentService, QuoteService
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum, F, FloatField
from django.db.models.functions import ExtractYear
from statistics import median, mode
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

class PizzaListView(ListView):
    model = Pizza
    template_name = 'pizza/pizza_list.html'
    context_object_name = 'pizzas'

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'pizza/pizza_detail.html'
    context_object_name = 'pizza'

class PizzaCreateView(UserPassesTestMixin, CreateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza_list')
    login_url = 'pizza:login'

    def test_func(self):
        return self.request.user.is_superuser

class PizzaUpdateView(UserPassesTestMixin, UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza_list')

    def test_func(self):
        return self.request.user.is_superuser

class PizzaDeleteView(UserPassesTestMixin, DeleteView):
    model = Pizza
    template_name = 'pizza/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza_list')

    def test_func(self):
        return self.request.user.is_superuser

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'pizza/order_form.html'
    success_url = reverse_lazy('pizza:order_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizzas'] = Pizza.objects.all()
        weather_service = WeatherService()
        weather = weather_service.get_weather()
        if weather:
            context['weather'] = weather
        return context

    def form_valid(self, form):
        try:
            order = form.save(commit=False)
            order.customer = self.request.user.customer
            order.status = 'pending'
            order.total_price = 0
            order.save()

            total_price = 0
            pizzas = Pizza.objects.all()

            for pizza in pizzas:
                quantity = self.request.POST.get(f'quantity_{pizza.id}')
                size_id = self.request.POST.get(f'size_{pizza.id}')
                
                if quantity and size_id and int(quantity) > 0:
                    size = PizzaSize.objects.get(id=size_id)
                    pricing = PizzaPricing.objects.get(pizza=pizza, size=size)
                    
                    OrderItem.objects.create(
                        order=order,
                        pizza=pizza,
                        size=size,
                        quantity=int(quantity),
                        item_price=pricing.price * int(quantity)
                    )
                    total_price += pricing.price * int(quantity)

            if total_price == 0:
                messages.error(self.request, 'Выберите хотя бы одну пиццу')
                return self.form_invalid(form)

            order.total_price = total_price
            order.save()
            messages.success(self.request, 'Заказ успешно создан!')
            return super().form_valid(form)
            
        except Exception as e:
            messages.error(self.request, f'Ошибка при создании заказа: {str(e)}')
            return self.form_invalid(form)

def order_complete(request):
    return render(request, 'pizza/order_complete.html', {
        'message': 'Ваш заказ успешно оформлен!'
    })

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'pizza/review_form.html'
    success_url = reverse_lazy('pizza:review_success')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        response = super().form_valid(form)
        messages.success(self.request, 'Спасибо за ваш отзыв!')
        return response

def review_success(request):
    return render(request, 'pizza/review_success.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pizza:pizza_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'pizza/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('pizza:pizza_list')

def create_payment_intent(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            payment_service = PaymentService()
            payment = payment_service.create_payment_intent(amount)
            return JsonResponse(payment)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def orders_by_month(request, year, month):
    orders = Order.objects.filter(
        order_date__year=year,
        order_date__month=month
    ).order_by('-order_date')
    
    context = {
        'orders': orders,
        'year': year,
        'month': month
    }
    return render(request, 'pizza/orders_by_month.html', context)

def orders_by_status(request, status):
    orders = Order.objects.filter(status=status).order_by('-order_date')
    context = {
        'orders': orders,
        'status': status
    }
    return render(request, 'pizza/orders_by_status.html', context)

def reviews_by_rating(request, rating):
    reviews = Review.objects.filter(rating=rating).order_by('-date')
    context = {
        'reviews': reviews,
        'rating': rating
    }
    return render(request, 'pizza/reviews_by_rating.html', context)

@staff_member_required
def statistics_view(request):
    # Получаем все завершенные заказы
    completed_orders = Order.objects.filter(Q(status='completed') | Q(status='delivered'))
    
    # Общие показатели
    total_sales = completed_orders.aggregate(
        total=Sum(F('total_price'))
    )['total'] or 0
    
    # Средний чек (используем все ненулевые заказы)
    non_zero_orders = completed_orders.filter(total_price__gt=0)
    avg_check = non_zero_orders.aggregate(
        avg=Avg('total_price')
    )['avg'] or 0
    
    # Медианный чек
    order_prices = list(non_zero_orders.values_list('total_price', flat=True))
    median_check = median(order_prices) if order_prices else 0
    
    # Топ-5 популярных пицц с учетом только завершенных заказов
    top_pizzas = OrderItem.objects.filter(
        order__in=completed_orders
    ).values(
        'pizza__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('item_price'))
    ).order_by('-total_quantity')[:5]

    # Статистика по категориям с учетом только завершенных заказов
    category_stats = OrderItem.objects.filter(
        order__in=completed_orders
    ).values(
        'pizza__category__name'
    ).annotate(
        pizzas_count=Count('pizza__id', distinct=True),
        total_sold=Sum('quantity'),
        total_revenue=Sum('item_price')
    ).order_by('-total_revenue')

    # Топ-10 клиентов по завершенным заказам
    top_customers = Order.objects.filter(
        id__in=completed_orders
    ).values(
        'customer__user__username'
    ).annotate(
        orders_count=Count('id'),
        total_spent=Sum('total_price')
    ).order_by('-total_spent')[:10]

    context = {
        'total_sales': total_sales,
        'avg_check': avg_check,
        'median_check': median_check,
        'top_pizzas': top_pizzas,
        'category_stats': category_stats,
        'top_customers': top_customers,
    }
    return render(request, 'admin/pizza/statistics.html', context)
