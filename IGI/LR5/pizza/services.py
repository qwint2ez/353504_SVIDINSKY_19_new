import requests
import stripe
from django.conf import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city="Minsk"):
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity']
            }
        return None

class PaymentService:
    @staticmethod
    def create_payment_intent(amount, currency='usd'):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Конвертируем в центы
                currency=currency,
            )
            return {
                'client_secret': intent.client_secret,
                'payment_id': intent.id
            }
        except Exception as e:
            return None
