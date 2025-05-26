from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q, Avg, Count, Sum, F, DecimalField, Value, Min, Max
from django.db.models.functions import Coalesce, TruncMonth, ExtractMonth, ExtractYear
from statistics import median, mode, mean
from calendar import month_name, monthcalendar
import pytz
from datetime import datetime, date
from .models import Pizza, Order, Review, OrderItem, PizzaSize, PizzaPricing, Customer, PizzaCategory
from .forms import PizzaForm, OrderForm, ReviewForm, UserRegistrationForm, PizzaPricingFormSet  # Добавляем импорт
from .services import WeatherService, PaymentService, QuoteService
from django.utils import timezone
import calendar
import matplotlib.pyplot as plt
import io
import base64
import logging

logger = logging.getLogger('pizza')

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
    success_url = reverse_lazy('pizza:pizza_create_success')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        try:
            context = self.get_context_data()
            pricing_formset = context['pricing_formset']
            if form.is_valid() and pricing_formset.is_valid():
                logger.info(f"Creating new pizza: {form.cleaned_data['name']}")
                self.object = form.save()
                pricing_formset.instance = self.object
                pricing_formset.save()
                logger.debug(f"Pizza created successfully with ID: {self.object.id}")
                messages.success(self.request, 'Пицца успешно создана!')
                return super().form_valid(form)
            logger.warning("Form validation failed")
            return self.render_to_response(self.get_context_data(form=form))
        except Exception as e:
            logger.error(f"Error creating pizza: {str(e)}")
            raise

    def form_invalid(self, form):
        logger.warning(f"Invalid form data: {form.errors}")
        return super().form_invalid(form)

# Add success view
def pizza_create_success(request):
    return render(request, 'pizza/pizza_create_success.html')

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
        
        # Добавляем погоду
        weather_service = WeatherService()
        weather = weather_service.get_weather()
        if weather:
            context['weather'] = weather
            
        # Добавляем цитату из Breaking Bad
        quote_service = QuoteService()
        quote = quote_service.get_quote()
        if quote:
            context['quote'] = quote
            
        return context

    def form_valid(self, form):
        try:
            logger.info(f'Starting order creation for user {self.request.user}')
            order = form.save(commit=False)
            order.customer = self.request.user.customer
            order.status = 'pending'
            order.save()
            logger.info(f'Order created: {order.id} by user {self.request.user}')

            total_price = 0
            has_items = False

            for pizza in Pizza.objects.all():
                quantity = int(self.request.POST.get(f'quantity_{pizza.id}', 0))
                size_id = self.request.POST.get(f'size_{pizza.id}')

                if quantity > 0 and size_id:
                    has_items = True
                    size = PizzaSize.objects.get(id=size_id)
                    try:
                        pricing = PizzaPricing.objects.get(pizza=pizza, size=size)
                        OrderItem.objects.create(
                            order=order,
                            pizza=pizza,
                            size=size,
                            quantity=quantity,
                            item_price=pricing.price * quantity
                        )
                        total_price += pricing.price * quantity
                    except PizzaPricing.DoesNotExist:
                        messages.error(self.request, f'Ошибка с ценой для пиццы {pizza.name}')
                        return self.form_invalid(form)

            if not has_items:
                messages.error(self.request, 'Выберите хотя бы одну пиццу')
                return self.form_invalid(form)

            order.total_price = total_price
            order.save()
            logger.info(f'Order {order.id} completed with total price: {total_price}')
            messages.success(self.request, 'Заказ успешно создан!')
            return super().form_valid(form)
        except Exception as e:
            logger.error(f'Error creating order: {str(e)}', exc_info=True)
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
            # Проверяем, есть ли уже профиль
            if not Customer.objects.filter(user=user).exists():
                Customer.objects.create(
                    user=user,
                    birth_date=form.cleaned_data['birth_date']
                )
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

def reviews_list(request):
    """Представление для отображения всех отзывов"""
    reviews = Review.objects.select_related(
        'customer__user', 
        'pizza'
    ).order_by('-date')
    return render(request, 'pizza/reviews.html', {'reviews': reviews})

@staff_member_required
def statistics_view(request):
    logger.info(f'Statistics viewed by user {request.user}')
    # Параметры сортировки и поиска
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    sort_direction = request.GET.get('direction', 'asc')

    # Базовый QuerySet для пицц
    all_pizzas = Pizza.objects.annotate(
        sales_count=Count('orderitem'),
        revenue=Coalesce(Sum('orderitem__item_price'), Value(0), 
                        output_field=DecimalField(max_digits=10, decimal_places=2))
    ).select_related('category')

    # Применяем поиск если есть запрос
    if search_query:
        all_pizzas = all_pizzas.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Определяем направление и поле сортировки
    sort_field = {
        'name_asc': 'name',
        'name_desc': '-name',
        'sales_asc': 'sales_count',
        'sales_desc': '-sales_count',
        'revenue_asc': 'revenue',
        'revenue_desc': '-revenue',
    }.get(f"{sort_by}_{sort_direction}", 'name')

    all_pizzas = all_pizzas.order_by(sort_field)

    # Получаем текущую дату для календаря
    current_date = datetime.now()
    cal = calendar.monthcalendar(current_date.year, current_date.month)
    month_name = calendar.month_name[current_date.month]

    # Общие показатели
    orders = Order.objects.all()
    total_sales = orders.aggregate(
        total=Coalesce(Sum('total_price'), Value(0), 
        output_field=DecimalField(max_digits=10, decimal_places=2))
    )['total']
    
    # Средний чек
    orders_with_price = orders.filter(total_price__gt=0)
    avg_check = orders_with_price.aggregate(
        avg=Coalesce(Avg('total_price'), Value(0), 
        output_field=DecimalField(max_digits=10, decimal_places=2))
    )['avg']

    # Медианный чек
    prices = list(orders_with_price.values_list('total_price', flat=True))
    median_check = median(prices) if prices else 0

    # Топ-5 популярных пицц
    top_pizzas = OrderItem.objects.values(
        'pizza__name'
    ).annotate(
        sales_count=Sum('quantity'),
        revenue=Sum(F('item_price'))
    ).order_by('-sales_count')[:5]

    # Статистика по категориям
    category_stats = OrderItem.objects.values(
        'pizza__category__name'
    ).annotate(
        pizzas_count=Count('pizza', distinct=True),
        sold=Sum('quantity'),
        revenue=Sum(F('item_price'))
    ).order_by('-revenue')

    # Топ-10 клиентов
    top_customers = Order.objects.values(
        'customer__user__username'
    ).annotate(
        orders_count=Count('id'),
        total_spent=Sum('total_price')
    ).order_by('-total_spent')[:10]

    # Создаем графики с помощью matplotlib
    def generate_bar_chart(labels, sales_data, revenue_data):
        plt.figure(figsize=(15, 8))
        plt.clf()
        plt.bar(labels, sales_data)
        plt.title('Топ-5 популярных пицц')
        plt.xticks(rotation=45)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')

    def generate_pie_chart(labels, values):
        plt.figure(figsize=(12, 12))
        plt.clf()
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('Распределение выручки по категориям')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')

    # Генерируем графики
    sales_chart = generate_bar_chart(
        [p['pizza__name'] for p in top_pizzas],
        [p['sales_count'] for p in top_pizzas],
        [float(p['revenue']) for p in top_pizzas]
    )

    category_chart = generate_pie_chart(
        [c['pizza__category__name'] for c in category_stats],
        [float(c['revenue']) for c in category_stats]
    )

    # Исправляем подсчет заказов за сегодня
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timezone.timedelta(days=1)
    orders_today = Order.objects.filter(
        order_date__gte=today_start,
        order_date__lt=today_end
    ).count()

    context = {
        'total_sales': total_sales,
        'avg_check': avg_check,
        'median_check': median_check,
        'top_pizzas': top_pizzas,
        'category_stats': category_stats,
        'top_customers': top_customers
    }
    
    context.update({
        'current_date': current_date.strftime('%d/%m/%Y'),
        'current_time': current_date.strftime('%H:%M:%S'),
        'utc_time': datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
        'calendar': cal,
        'month_name': month_name,
        'current_day': current_date.day,
        'orders_today': orders_today,
        'all_pizzas': all_pizzas,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'sales_chart': sales_chart,
        'category_chart': category_chart
    })
    
    return render(request, 'pizza/statistics.html', context)
