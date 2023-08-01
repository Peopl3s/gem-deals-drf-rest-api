import copy
import csv
import io
import os
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, Dict, List

from django.db import transaction
from django.db.models import Sum

from .models import Customer, Deal, Gem


class BaseReader(ABC):
    """Абстрактный базовый класс для чтения файлов различных форматов."""

    @abstractmethod
    def get_reader(self) -> Iterable:
        """Возвращает инстанс ридера для файла определённого формата."""
        pass


class CsvReader(BaseReader):
    """Класс для обработки csv-файлов."""

    def __init__(self, source_file: bytes) -> None:
        """Инициализация объекта.
        Args:
            source_file (bytes): Файла в байтовом виде для создания экзепляра ридера.
        Returns:
        """
        
        
        self._csvfile = io.StringIO(source_file.decode("utf-8"))
        self._reader = csv.reader(
            self._csvfile, self._get_dialect(source_file=source_file)
        )

    def _get_dialect(self, source_file: bytes|str) -> csv.Dialect | None:
        """Возвращает csv.Dialect для автоматического определения delimiter и escapechar.
        Args:
            source_file (bytes): Файла в байтовом виде для создания экзепляра ридера.
        Returns:
            csv.Dialect | None: Диалет csv или None, если невозможно определить диалект.
            https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters
        """

        if not isinstance(source_file, str):
            source_file = str(source_file)
        dialect = csv.Sniffer().sniff(source_file, delimiters=";,|")
        return dialect

    def get_reader(self) -> csv.DictReader:
        """Возвращает _csv.reader из которого можно получить доступ к csv.DictReader."""

        return self._reader


def get_data_from_file(
    filename: str, file_content: bytes
) -> List[Dict[str, str]] | None:
    """Возвращает содержимое файла.
    Args:
        filename (str): Название файла.
        file_content (bytes): Файла в байтовом виде.
    Returns:
        List[Dict[str, str]] | None: Содержимое файла или None, если файл невозможно обработать.
    """
    data = None
    reader_descriptor: BaseReader | None = _get_reader_file_descriptor(
        filename, file_content
    )
    if reader_descriptor:
        data = get_data_from_reader(reader_descriptor)
    return data


def _get_reader_file_descriptor(filename: str, file: bytes) -> BaseReader | None:
    """Возвращает соответствующий формату файла ридер.
    Args:
        filename (str): Название файла.
        file_content (bytes): Файла в байтовом виде.
    Returns:
        BaseReader | None: Ридер для файла или None, если файл невозможно обработать.
    """

    reader_descriptor = None
    file_extension:str = _get_file_extension(filename)
    if file_extension == ".csv":
        try:
            reader_descriptor = CsvReader(source_file=file)
        except csv.Error:
            return None
    return reader_descriptor


def _get_file_extension(file_path: str) -> str:
    """Возвращает расширение файла.
    Args:
        file_path (str): Путь до файла.
    Returns:
        str: Расширение файла или пустая строка, если расширение невозможно получить.
    """

    _, file_extension = os.path.splitext(file_path)
    return file_extension


def get_data_from_reader(reader_descriptor: BaseReader) -> List[Dict[str, str]] | None:
    """Возвращает данные из загруженного файла.
    Args:
        reader_descriptor (BaseReader): Ридер соответствующий формату файла.
    Returns:
        List[Dict[str, str]] | None: Данные из файла или None, если файл невозможно обработать.
    """

    reader = reader_descriptor.get_reader()
    if not reader:
        return None
    data = []
    header: List[str] = next(reader)
    for row in reader:
        data.append({key: value for key, value in zip(header, row)})
    return data


def save_data_in_db(deals: List[Dict[str, str]]) -> None:
    """Сохраняет данные из списка deals в базу данных.
    Args:
        deals (List[Dict[str, str]]): Список с информацией о сделках.
    Returns:
    """
    with transaction.atomic():
        _clear_db_data()
        for deal in deals:
            customer, _ = Customer.objects.get_or_create(username=deal["customer"])
            gem, _ = Gem.objects.get_or_create(name=deal["item"])
            Deal.objects.create(
                customer=customer,
                item=gem,
                total=deal["total"],
                quantity=deal["quantity"],
                date=deal["date"],
            )


def _clear_db_data() -> None:
    """Очищает содержимое базы данных
    (объекты Deal удалятся автоматически т.к. связаны с Gem и Customer).
    Args:
    Returns:
    """
    Customer.objects.all().delete()
    Gem.objects.all().delete()


def get_customer_data(customers: List[Dict[str, str]], field: str) -> List[str]:
    """Получает список со значениями ключа field из словарей списка customers.
    Args:
        customers (List[Dict[str, str]]): Список клиентов (каждый клиент представле Dict).
        field (str): Ключ, значение котого необходимо получить из списка словарей
    Returns:
        List[str] | None: Список значений ключа field или None, если файл невозможно обработать.
    """
    
    
    field_values = []
    for customer in customers:
        field_values.append(customer[field])
    return field_values


def get_largest_amount_customers(limit: int) -> List[Dict[str, Any]]:
    """Возвращает список клиентов, потративших наибольшую сумму за весь период.
     Args:
        limit (int): Количество клиентов, которые нужно получить из БД.
    Returns:
        List[Dict[str, Any]]: Список клиентов в виде словарей.
    """

    largest_amount_customers = (
        Deal.objects.values("customer", "customer__username")
        .annotate(spent_money=Sum("total"))
        .order_by("-spent_money")[:limit]
    )
    return list(largest_amount_customers)


def get_customer_gems(customer_id: str) -> "ValuesQuerySet[Gem, Any]":
    """Возвращает список драгоценных камней, пренадлежащих определённому клиенту.
     Args:
        customer_id (str): ID клиента.
    Returns:
        ValuesQuerySet[Gem, Any]: Набор драгоценных камней клиента.
    """

    return (
        Gem.objects.prefetch_related("gem_customers")
        .filter(customers=customer_id)
        .values_list("name", flat=True)
        .distinct()
    )


def get_same_customer_gems(
    customers_ids: List[str], find_gems: "ValuesQuerySet[Gem, Any]"
) -> List[Gem]:
    """Возвращает драгоценные камни из определённого перечня.
     Args:
        customers_ids (List[str]): ID клиентов, которым пренадлежат камни.
        find_gems (ValuesQuerySet[Gem, Any]): Набор камней, названия которых должны быть в результирующей выборке.
    Returns:
        List[Gem]: Драгоценные камни, которые есть у покупателей из списка customers_ids и названия которых пересекаются
        со списком камней в find_gems.
    """
    return list(
        Gem.objects.prefetch_related("gem_customers")
        .filter(customers__in=customers_ids, name__in=find_gems)
        .distinct()
    )


def add_gems_field_to_customers_data(customers: List[Dict[str, Any]]) -> None:
    """Добавляет в информацию о клиенте - данные, о купленных им камнях, которые также есть
    у других клиентов из списка "Потративших наибольшую сумму за весь период".
     Args:
        customers: List[Dict[str, Any]]: Данные о клиентах из списка "Потративших наибольшую сумму за весь период".
    Returns:
    """

    customers_ids:List[str] = get_customer_data(customers, "customer")
    for id in customers_ids:
        tmp_ids = copy.copy(customers_ids)
        tmp_ids.remove(id)
        current_customer_gems:"ValuesQuerySet[Gem, Any]" = get_customer_gems(id)
        gems_other_customers_have:List[Gem] = get_same_customer_gems(tmp_ids, current_customer_gems)
        for customer in customers:
            if customer["customer"] == id:
                customer["gems"] = gems_other_customers_have
