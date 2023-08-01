from django.test import TestCase

from ..models import Gem
from ..serializers import CustomerSerializer


class TestSerializers(TestCase):
    """Тестирование сериализатора для результирующего набора клиентов."""

    def setUp(self):
        """Создаёт входные данные для тестов."""
        
        
        self.serialized_obj = {
            "username": "resplendent",
            "spent_money": 451731,
            "gems": ["Сапфир", "Рубин", "Танзанит"],
        }

    def test_result_customer_serializers(self):
        """Тест на корректную сериализацию результирующей информации о клиенте."""
        
        
        customer = {
            "customer": "38",
            "customer__username": "resplendent",
            "spent_money": 451731,
            "gems": [Gem(name="Сапфир"), Gem(name="Рубин"), Gem(name="Танзанит")],
        }
        self.assertEqual(self.serialized_obj, CustomerSerializer(customer).data)
