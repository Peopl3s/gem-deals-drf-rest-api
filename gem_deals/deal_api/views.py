import logging

from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerSerializer
from .services import *

logger = logging.getLogger(__name__)


class DealAPIView(APIView):
    """Представление для обработки входящих запросов."""

    def get(self, request, format=None) -> Response:
        """Обрабатывает входящий GET-запрос на выдачу обработанных данных.

        Returns:
            Response: Объект Response, содержащий поле "response"
            со списком из 5 клиентов, потративших наибольшую сумму за весь период.
        """

        customers = cache.get(settings.CACHE_PREFIX)
        if customers is None:
            customers = get_largest_amount_customers(settings.GET_ROWS_LIMIT)
            cache.set(settings.CACHE_PREFIX, customers, settings.CACHE_TTL_SECONDS)
        add_gems_field_to_customers_data(customers)
        serializer = CustomerSerializer(data=customers, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response({"response": serializer.data}, status=200)

    def post(self, request, format=None) -> Response:
        """Обрабатывает входящий POST-запрос,
        принимает из POST-запроса .csv файл для дальнейшей обработки.

        Returns:
            Response: Объект Response, содержащий:
            Status: OK - если файл был обработан без ошибок;
            Status: Error, Desc: <Описание ошибки> - если в процессе обработки файла произошла ошибка.
        """

        if request.FILES:
            for _, file in request.FILES.items():
                deals = get_data_from_file(filename=str(file), file_content=file.read())
                if deals:
                    save_data_in_db(deals)
                    cache.clear()
                else:
                    logger.warning(f"Попытка обработки некорректного csv-файла.")
                    return Response(
                        {
                            "Status": "Error",
                            "Desc": "Расширение файла не csv либо содержимое файла не является валидным csv.",
                        },
                        status=400,
                    )
        else:
            logger.warning(f"Запрос не содержит файл.")
            return Response({"Status": "Error", "Desc": "Отсутствует файл"}, status=400)
        return Response({"Status": "OK"}, status=200)
