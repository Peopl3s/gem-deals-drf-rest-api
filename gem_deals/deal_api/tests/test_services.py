from django.test import TestCase

from ..models import Customer, Deal, Gem
from ..services import (_get_file_extension, add_gems_field_to_customers_data,
                        get_customer_gems, get_largest_amount_customers)


class TestServices(TestCase):
    """Тестирование вспомогательных функций."""

    def setUp(self) -> None:
        """Создаёт входные данные для тестов."""
        
        
        self.customer = Customer.objects.create(username="test")
        self.customer2 = Customer.objects.create(username="test2")
        self.gem1 = Gem.objects.create(name="test_gem1")
        self.gem2 = Gem.objects.create(name="test_gem2")
        self.deal1 = Deal.objects.create(
            customer=self.customer,
            item=self.gem1,
            total=5000,
            quantity=2,
            date="2023-08-01 12:00:00",
        )
        self.deal2 = Deal.objects.create(
            customer=self.customer,
            item=self.gem2,
            total=7000,
            quantity=3,
            date="2023-08-01 12:01:00",
        )
        self.deal3 = Deal.objects.create(
            customer=self.customer2,
            item=self.gem2,
            total=1000,
            quantity=3,
            date="2023-08-01 12:03:00",
        )

    def test_get_file_extension(self) -> None:
        """Тест определения расширения файла."""
        
        
        extension1 = _get_file_extension("deals.csv")
        extension2 = _get_file_extension("deals.tmp.csv")
        extension3 = _get_file_extension("deals")
        self.assertEqual(extension1, ".csv")
        self.assertEqual(extension2, ".csv")
        self.assertEqual(extension3, "")

    def test_get_customer_gems(self) -> None:
        """Тест получение камней клиента."""
        
        
        gems = get_customer_gems(self.customer.id)
        self.assertEqual(len(gems), 2)
        self.assertEqual(str(gems[0]), "test_gem1")
        self.assertEqual(str(gems[1]), "test_gem2")

    def test_get_largest_amount_customers(self) -> None:
        """Тест получение списка клиентов, потративших наибольшее количество денег."""
        
        
        customers = get_largest_amount_customers(limit=1)
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["customer"], 1)
        self.assertEqual(customers[0]["spent_money"], 12000)

    def test_add_gems_field_to_customers_data(self) -> None:
        """Тест на добавление списка камней в данные о клиенте."""
        
        
        customers = get_largest_amount_customers(limit=2)
        add_gems_field_to_customers_data(customers)
        self.assertEqual(len(customers[0]["gems"]), 1)
