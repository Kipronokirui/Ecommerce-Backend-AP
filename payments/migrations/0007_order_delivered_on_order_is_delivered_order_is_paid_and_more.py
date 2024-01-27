# Generated by Django 4.2.9 on 2024-01-14 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0006_alter_orderitem_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivered_on",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="order",
            name="is_delivered",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="ordered_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
