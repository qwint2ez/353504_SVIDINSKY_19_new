from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pizza, Order, Review
from .forms import PizzaForm, OrderForm, ReviewForm, UserRegistrationForm
from .services import WeatherService, PaymentService
from django.http import JsonResponse
from django.conf import settings

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
    success_url = reverse_lazy('pizza:order_success')
    login_url = 'pizza:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_service = WeatherService()
        weather = weather_service.get_weather()
        if weather:
            context['weather'] = weather
        context['stripe_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def form_valid(self, form):
        # Создаем платёжное намерение
        payment_service = PaymentService()
        payment = payment_service.create_payment_intent(
            amount=form.instance.total_price
        )
        if payment:
            form.instance.payment_id = payment['payment_id']
            return super().form_valid(form)
        return self.form_invalid(form)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'pizza/review_form.html'
    success_url = reverse_lazy('pizza:review_success')
    login_url = 'pizza:login'

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)

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
