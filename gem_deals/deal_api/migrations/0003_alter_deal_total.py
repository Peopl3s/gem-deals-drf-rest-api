# Generated by Django 4.2.3 on 2023-08-01 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("deal_api", "0002_alter_deal_customer_alter_deal_item_alter_deal_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="total",
            field=models.DecimalField(
                decimal_places=2, max_digits=8, verbose_name="Сумма сделки"
            ),
        ),
    ]
