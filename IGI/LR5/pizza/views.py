from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Pizza, Order, Review
from .forms import PizzaForm, OrderForm, ReviewForm

class PizzaListView(ListView):
    model = Pizza
    template_name = 'pizza/pizza_list.html'
    context_object_name = 'pizzas'

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'pizza/pizza_detail.html'
    context_object_name = 'pizza'

class PizzaCreateView(CreateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza_list')

class PizzaUpdateView(UpdateView):
    model = Pizza
    form_class = PizzaForm
    template_name = 'pizza/pizza_form.html'
    success_url = reverse_lazy('pizza_list')

class PizzaDeleteView(DeleteView):
    model = Pizza
    template_name = 'pizza/pizza_confirm_delete.html'
    success_url = reverse_lazy('pizza_list')

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'pizza/order_form.html'
    success_url = reverse_lazy('pizza:order_success')

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'pizza/review_form.html'
    success_url = reverse_lazy('pizza:review_success')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)
