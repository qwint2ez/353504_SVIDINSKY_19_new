from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
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
from .models import Pizza, Order, Review, OrderItem, PizzaSize, PizzaPricing, Customer, PizzaCategory, Article, Promo, Courier, CompanyInfo, FAQ, Vacancy, Banner, PartnerCompany, Cart, CartItem
from .forms import PizzaForm, OrderForm, ReviewForm, UserRegistrationForm, PizzaPricingFormSet  # Добавляем импорт
from .services import WeatherService, PaymentService, QuoteService
from django.utils import timezone
import calendar
import matplotlib.pyplot as plt
import io
import base64
import logging
from .decorators import api_login_required

logger = logging.getLogger('pizza')

class HomeView(TemplateView):
    template_name = 'pizza/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_logo'] = CompanyInfo.objects.first().logo if CompanyInfo.objects.first() else None
        context['banners'] = Banner.objects.filter(is_active=True)
        context['catalog'] = Pizza.objects.all()  # Можно заменить на услуги/товары
        context['latest_article'] = Article.objects.order_by('-created_date').first()
        context['partners'] = PartnerCompany.objects.all()
        # Добавляем активные акции и популярные пиццы
        context['promos'] = Promo.objects.filter(
            is_active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        )
        context['popular_pizzas'] = Pizza.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:6]
        return context

class MenuView(ListView):
    model = Pizza
    template_name = 'pizza/menu.html'
    context_object_name = 'pizzas'

    def get_queryset(self):
        queryset = Pizza.objects.all()
        category = self.request.GET.get('category')
        sauce = self.request.GET.get('sauce')
        is_vegan = self.request.GET.get('is_vegan')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if category:
            queryset = queryset.filter(category_id=category)
        if sauce:
            queryset = queryset.filter(sauce=sauce)
        if is_vegan:
            queryset = queryset.filter(is_vegan=True)
        if min_price:
            queryset = queryset.filter(pizzapricing__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(pizzapricing__price__lte=max_price)

        logger.debug(f'Menu filter params: category={category}, sauce={sauce}, is_vegan={is_vegan}, price={min_price}-{max_price}')
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PizzaCategory.objects.all()
        context['sauces'] = Pizza.objects.values_list('sauce', flat=True).distinct()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_sauce'] = self.request.GET.get('sauce')
        context['is_vegan'] = self.request.GET.get('is_vegan')
        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        return context

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'pizza/pizza_detail.html'
    context_object_name = 'pizza'

class ProductDetailView(DetailView):
    model = Pizza
    template_name = 'pizza/product_detail.html'
    context_object_name = 'pizza'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_to_cart'] = self.request.user.is_authenticated
        return context

class PizzaCreateView(UserPassesTestMixin, CreateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza:menu')  # Изменено с pizza_create_success на menu

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        try:
            logger.debug(f'Starting pizza creation process by user {self.request.user}')
            self.object = form.save()
            logger.info(f"Pizza created successfully with ID: {self.object.id}")
            messages.success(self.request, 'Пицца успешно создана!')
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error creating pizza: {str(e)}")
            messages.error(self.request, f'Ошибка при создании пиццы: {str(e)}')
            return self.form_invalid(form)

# Add success view
def pizza_create_success(request):
    return render(request, 'pizza/pizza_create_success.html')

class PizzaUpdateView(UserPassesTestMixin, UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza:menu')  # Изменено с pizza_list на menu

    def test_func(self):
        return self.request.user.is_superuser

class PizzaDeleteView(UserPassesTestMixin, DeleteView):
    model = Pizza
    template_name = 'pizza/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza:menu')  # Изменено с pizza_list на menu

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
            logger.debug(f'Starting order creation process for user {self.request.user}')
            order = form.save(commit=False)
            order.customer = self.request.user.customer
            order.status = 'pending'
            
            # Убедимся, что delivery_date в UTC
            delivery_date = form.cleaned_data.get('delivery_date')
            if timezone.is_naive(delivery_date):
                delivery_date = timezone.make_aware(delivery_date)
            order.delivery_date = delivery_date
            
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

@login_required
def update_order_status(request, order_id):  # Изменили pk на order_id
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)  # Используем order_id
            status = request.POST.get('status')
            courier_id = request.POST.get('courier_id')
            
            if status in dict(Order.STATUS_CHOICES):
                order.status = status
                if courier_id:
                    order.courier = get_object_or_404(Courier, id=courier_id)
                order.save()
                logger.info(f'Order {order_id} status updated to {status} by {request.user}')
                messages.success(request, 'Статус заказа успешно обновлен')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success'})
                return redirect('pizza:orders_list')
            else:
                messages.error(request, 'Некорректный статус заказа')
        except Exception as e:
            logger.error(f'Error updating order status: {str(e)}')
            messages.error(request, 'Произошла ошибка при обновлении статуса')
    return redirect('pizza:orders_list')

# Добавляем представления для отзывов
def reviews_list(request):
    reviews = Review.objects.select_related('customer__user', 'pizza').order_by('-date')
    return render(request, 'pizza/reviews_list.html', {'reviews': reviews})

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'pizza/review_form.html'
    success_url = reverse_lazy('pizza:reviews_list')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        response = super().form_valid(form)
        messages.success(self.request, 'Спасибо за ваш отзыв!')
        return response

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
            return redirect('pizza:menu')  # Меняем на menu
    else:
        form = UserRegistrationForm()
    return render(request, 'pizza/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('pizza:menu')  # изменено с pizza_list на menu

def promo_list(request):
    current_time = timezone.now()
    active_promos = Promo.objects.filter(
        is_active=True,
        valid_from__lte=current_time,
        valid_to__gte=current_time
    )
    return render(request, 'pizza/promo_list.html', {'promos': active_promos})

@api_login_required
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            logger.debug('Starting payment intent creation')
            amount = float(request.POST.get('amount'))
            payment_service = PaymentService()
            payment = payment_service.create_payment_intent(amount)
            logger.info(f'Payment intent created for amount: {amount}')
            return JsonResponse(payment)
        except Exception as e:
            logger.error(f'Payment intent creation failed: {str(e)}', exc_info=True)
            return JsonResponse({'error': str(e)}, status=400)
    logger.warning('Invalid payment request method')
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
    try:
        logger.debug('Starting statistics calculation')
        
        # Используем timezone.now() вместо datetime.now()
        current_date = timezone.now()
        
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
        
        logger.info(f'Statistics viewed by user {request.user}')
        return render(request, 'pizza/statistics.html', context)
    except Exception as e:
        logger.error(f'Error generating statistics: {str(e)}', exc_info=True)
        messages.error(request, 'Ошибка при формировании статистики')
        return redirect('pizza:pizza_list')

class OrdersListView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'pizza/orders_list.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['couriers'] = Courier.objects.all()
        context['status_choices'] = Order.STATUS_CHOICES
        return context

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')

class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'pizza/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer).order_by('-created_at')

class CouriersListView(UserPassesTestMixin, ListView):
    model = Courier 
    template_name = 'pizza/couriers_list.html'  # Make sure template name matches
    context_object_name = 'couriers'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Courier.objects.all().order_by('user__username')

def promotions_view(request):
    current_time = timezone.now()
    public_promos = Promo.objects.filter(
        is_active=True,
        valid_from__lte=current_time,
        valid_to__gte=current_time
    )
    
    context = {
        'public_promos': public_promos,
    }
    
    if request.user.is_authenticated:
        try:
            # Проверяем, есть ли у пользователя профиль Customer
            if hasattr(request.user, 'customer'):
                active_promos = request.user.customer.promos.filter(
                    is_active=True,
                    valid_to__gte=current_time
                )
                context['active_promos'] = active_promos
        except Customer.DoesNotExist:
            # Если профиля нет, просто не добавляем активные промокоды в контекст
            pass
    
    return render(request, 'pizza/promotions.html', context)

@login_required
def apply_promo(request):
    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo = Promo.objects.get(
                code=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            promo.customers.add(request.user.customer)
            messages.success(request, 'Промокод успешно применен!')
        except Promo.DoesNotExist:
            messages.error(request, 'Недействительный промокод')
    return redirect('pizza:promotions')

@login_required
def update_order_status(request, order_id):  # Изменили pk на order_id
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, id=order_id)  # Используем order_id
            status = request.POST.get('status')
            courier_id = request.POST.get('courier_id')
            
            if status in dict(Order.STATUS_CHOICES):
                order.status = status
                if courier_id:
                    order.courier = get_object_or_404(Courier, id=courier_id)
                order.save()
                logger.info(f'Order {order_id} status updated to {status} by {request.user}')
                messages.success(request, 'Статус заказа успешно обновлен')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success'})
                return redirect('pizza:orders_list')
            else:
                messages.error(request, 'Некорректный статус заказа')
        except Exception as e:
            logger.error(f'Error updating order status: {str(e)}')
            messages.error(request, 'Произошла ошибка при обновлении статуса')
    return redirect('pizza:orders_list')

@login_required
def assign_courier(request, order_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            order = get_object_or_404(Order, id=order_id)
            courier_id = request.POST.get('courier_id')
            
            if courier_id:
                courier = Courier.objects.get(id=courier_id)
                order.courier = courier
                order.save()
                logger.info(f'Courier {courier.user.username} assigned to order {order_id}')
                return JsonResponse({
                    'status': 'success',
                    'message': 'Курьер успешно назначен'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Не указан ID курьера'
                }, status=400)
        except Courier.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Курьер не найден'
            }, status=404)
        except Exception as e:
            logger.error(f'Error assigning courier: {str(e)}')
            return JsonResponse({
                'status': 'error',
                'message': 'Произошла ошибка при назначении курьера'
            }, status=500)
    return JsonResponse({
        'status': 'error',
        'message': 'Неверный запрос'
    }, status=400)

class ArticleListView(ListView):
    model = Article
    template_name = 'pizza/news.html'
    context_object_name = 'articles'
    ordering = ['-created_date']

def review_success(request):
    return render(request, 'pizza/review_success.html', {
        'message': 'Спасибо за ваш отзыв!'
    })

def about_view(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'pizza/about.html', {'company_info': company_info})

def faq_view(request):
    faqs = FAQ.objects.all().order_by('-date_added')
    return render(request, 'pizza/faq.html', {'faqs': faqs})

def contacts_view(request):
    return render(request, 'pizza/contacts.html')

def jobs_view(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'pizza/jobs.html', {'vacancies': vacancies})

def privacy_policy(request):
    logger.info(f"Privacy policy viewed by {request.user}")
    return render(request, 'pizza/privacy_policy.html')

from django.views import View

class CartView(LoginRequiredMixin, View):
    template_name = 'pizza/cart.html'

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'cart': cart})

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        if action == 'delete' and item_id:
            CartItem.objects.filter(id=item_id, cart=cart).delete()
        elif action in ['increase', 'decrease'] and item_id:
            item = CartItem.objects.get(id=item_id, cart=cart)
            if action == 'increase':
                item.quantity += 1
            elif action == 'decrease' and item.quantity > 1:
                item.quantity -= 1
            item.save()
        return redirect('pizza:cart')

@login_required
def add_to_cart(request, pizza_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    pizza = get_object_or_404(Pizza, id=pizza_id)
    item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('pizza:cart')

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'pizza/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        context['cart'] = cart
        return context
