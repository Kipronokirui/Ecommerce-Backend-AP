# Generated by Django 4.2.9 on 2024-01-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_remove_manufacturingcompany_sub_category_and_more"),
        ("payments", "0003_alter_orderitem_order"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together={("order", "product")},
        ),
    ]
