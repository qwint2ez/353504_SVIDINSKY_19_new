try:
    import requests
except ImportError:
    requests = None

try:
    import stripe
except ImportError:
    stripe = None

from django.conf import settings

class WeatherService:
    def __init__(self):
        self.api_key = '637561259c85a9aca793fa024f9a61e0'
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city="Minsk"):
        if not requests:
            print("requests module not available")
            return None
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'ru'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()  # Will raise an exception for 4XX/5XX errors
            
            data = response.json()
            return {
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        except Exception as e:
            print(f"Ошибка получения погоды: {str(e)}")
            return None

class PaymentService:
    def __init__(self):
        if not stripe:
            print("stripe module not available")
            return
        self.stripe_public_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
        self.stripe_secret_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        stripe.api_key = self.stripe_secret_key

    def create_payment_intent(self, amount):
        if not stripe:
            print("stripe module not available")
            return None
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Конвертируем в центы
                currency='usd',
                payment_method_types=['card'],
            )
            return {
                'client_secret': intent.client_secret,
                'payment_id': intent.id
            }
        except Exception as e:
            print(f"Stripe error: {str(e)}")
            return None

class QuoteService:
    def __init__(self):
        self.base_url = "https://api.breakingbadquotes.xyz/v1/quotes"

    def get_quote(self):
        if not requests:
            print("requests module not available")
            return None
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {
                        'quote': data[0]['quote'],
                        'author': data[0]['author']
                    }
        except Exception as e:
            print(f"Ошибка получения цитаты: {e}")
        return None
