import json

from django.test import Client, TestCase
from rest_framework import status


class TestDealViewApi(TestCase):
    """Набор тестов для views."""

    def setUp(self) -> None:
        """Создаёт входные данные для тестов."""
        self.client = Client()
        self.API_URL = "http://127.0.0.1:8000/api/v1/"
        self.file = open("deals.csv", "r", encoding="utf-8")
        self.correct_result = {
            "response": [
                {
                    "username": "resplendent",
                    "spent_money": 451731,
                    "gems": ["Сапфир", "Рубин", "Танзанит"],
                },
                {
                    "username": "bellwether",
                    "spent_money": 217794,
                    "gems": ["Сапфир", "Петерсит"],
                },
                {
                    "username": "uvulaperfly117",
                    "spent_money": 120419,
                    "gems": ["Петерсит", "Танзанит"],
                },
                {
                    "username": "braggadocio",
                    "spent_money": 108957,
                    "gems": ["Изумруд"],
                },
                {
                    "username": "turophile",
                    "spent_money": 100132,
                    "gems": ["Рубин", "Изумруд"],
                },
            ]
        }

    def test_get_request_correct_with_empty_db(self):
        """Тест на получение корректного ответа если БД пуста."""
        
        
        response = self.client.get(self.API_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "response")

    def test_post_request_without_csvfile(self):
        """Тест на получение корректного ответа если в теле запроса нет файла."""
        
        
        response = self.client.post(self.API_URL, {"deal": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_incorrect_file_exstension(self):
        """Тест на получение корректного ответа если в теле запроса не csv-файл."""
        
        
        response = self.client.post(self.API_URL, {"deal": "deal.cpp"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_csvfile_mutlipart_format(self):
        """Тест на получение корректного ответа формат отправки данных mutlipart."""
        
        
        data = {"deals": self.file}
        response = self.client.post(self.API_URL, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_csvfile_json_format(self):
        """Тест на получение корректного ответа формат отправки данных json."""
        
        
        data = {"deals": self.file}
        response = self.client.post(self.API_URL, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_csvfile_urlencode_format(self):
        """Тест на получение корректного ответа формат отправки данных x-www-urlencode."""
        
        
        data = {"deals": self.file}
        response = self.client.post(
            self.API_URL, data, format="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correct_result(self):
        """Тест на получение корректного ответа если данные загружены."""
        
        
        data = {"deals": self.file}
        response = self.client.post(
            self.API_URL, data, format="application/x-www-form-urlencoded"
        )
        response2 = self.client.get(self.API_URL)
        json_data_response = json.loads(response2.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(json_data_response, self.correct_result)
