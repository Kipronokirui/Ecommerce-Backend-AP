# Generated by Django 4.2.9 on 2024-01-12 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_alter_orderitem_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together=set(),
        ),
    ]
