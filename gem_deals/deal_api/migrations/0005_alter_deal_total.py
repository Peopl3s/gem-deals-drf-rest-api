# Generated by Django 4.2.3 on 2023-08-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("deal_api", "0004_alter_deal_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="total",
            field=models.IntegerField(verbose_name="Сумма сделки"),
        ),
    ]
