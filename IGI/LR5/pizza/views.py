from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum, F, DecimalField, Value
from django.db.models.functions import Coalesce, Cast
from statistics import median
from django.contrib.admin.views.decorators import staff_member_required
from .models import Pizza, Order, Review, OrderItem, PizzaSize, PizzaPricing, Customer, PizzaCategory
from .forms import PizzaForm, OrderForm, ReviewForm, UserRegistrationForm
from .services import WeatherService, PaymentService, QuoteService

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
    # Получаем все заказы
    orders = Order.objects.all()
    
    # Общие показатели
    total_sales = orders.aggregate(
        total=Coalesce(Sum('total_price'), Value(0), 
        output_field=DecimalField(max_digits=10, decimal_places=2))
    )['total']
    
    # Средний чек - только для заказов с суммой больше 0
    avg_check = orders.filter(
        total_price__gt=0
    ).aggregate(
        avg=Coalesce(Avg('total_price'), Value(0), 
        output_field=DecimalField(max_digits=10, decimal_places=2))
    )['avg'] or 0

    # Медианный чек
    order_amounts = list(orders.filter(
        total_price__gt=0
    ).values_list('total_price', flat=True))
    median_check = median(order_amounts) if order_amounts else 0

    # Топ-5 популярных пицц
    top_pizzas = Pizza.objects.annotate(
        sales_count=Count('orderitem'),
        revenue=Sum('orderitem__item_price')
    ).order_by('-sales_count')[:5]

    # Статистика по категориям
    category_stats = PizzaCategory.objects.annotate(
        pizzas_count=Count('pizza', distinct=True),
        total_sold=Count('pizza__orderitem'),
        revenue=Sum('pizza__orderitem__item_price', default=0)
    )

    # Топ-10 клиентов
    top_customers = Customer.objects.annotate(
        orders_count=Count('order'),
        total_spent=Sum('order__total_price', default=0)
    ).filter(
        total_spent__gt=0
    ).order_by('-total_spent')[:10]

    context = {
        'total_sales': total_sales,
        'avg_check': avg_check,
        'median_check': median_check,
        'top_pizzas': top_pizzas,
        'category_stats': category_stats,
        'top_customers': top_customers,
    }
    
    return render(request, 'pizza/statistics.html', context)
