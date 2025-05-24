from django.contrib import admin
from .models import *

class PizzaPricingInline(admin.TabularInline):
    model = PizzaPricing
    extra = 1

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'get_ingredients')
    list_filter = ('category', 'ingredients', 'allergens')
    search_fields = ('name', 'description')
    filter_horizontal = ('ingredients', 'allergens', 'recommended_with')
    inlines = [PizzaPricingInline]

    def get_ingredients(self, obj):
        return ", ".join([i.name for i in obj.ingredients.all()])
    get_ingredients.short_description = 'Ингредиенты'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'order_date')
    list_filter = ('status', 'payment_status', 'order_date')
    search_fields = ('customer__user__username', 'id')
    date_hierarchy = 'order_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'pizza', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('text', 'customer__user__username')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_vegetarian')
    list_filter = ('is_vegetarian',)
    search_fields = ('name', 'description')

@admin.register(PizzaCategory)
class PizzaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_date'

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'founding_year')
    filter_horizontal = ('employees',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'date_added')
    search_fields = ('question', 'answer')
    date_hierarchy = 'date_added'

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

# Регистрация остальных моделей
admin.site.register(Allergen)
admin.site.register(PizzaSize)
admin.site.register(Courier)
admin.site.register(OrderItem)
admin.site.register(CustomerPreferences)
admin.site.register(Employee)
admin.site.register(SeasonalPeriod)
