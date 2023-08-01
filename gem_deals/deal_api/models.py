from django.db import models


class Gem(models.Model):
    """Модель для драгоценных камней (предмет сделки)."""

    name = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Строка, представляющая название драгоценного камня",
    )

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    """Модель для клиентов."""

    username = models.CharField(max_length=255, verbose_name="Логин покупателя")
    gems = models.ManyToManyField(
        Gem,
        through="Deal",
        related_name="customers",
        null=True,
        verbose_name="Приобретённые драгоценные камни",
    )

    def __str__(self) -> str:
        return self.username


class Deal(models.Model):
    """Модель для сделок."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="customer_gems",
        verbose_name="Логин покупателя",
    )
    item = models.ForeignKey(
        Gem,
        on_delete=models.CASCADE,
        related_name="gem_customers",
        verbose_name="Наименование товара",
    )
    total = models.IntegerField(verbose_name="Сумма сделки")
    quantity = models.IntegerField(verbose_name="Количество товара, шт.")
    date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата и время регистрации сделки",
    )

    def __str__(self) -> str:
        return f"{self.date} : {self.customer} купил {self.item} ({self.quantity} шт.). Итог:{self.total}"
