# Generated by Django 4.2.3 on 2023-08-01 11:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("deal_api", "0003_alter_deal_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="total",
            field=models.FloatField(verbose_name="Сумма сделки"),
        ),
    ]
