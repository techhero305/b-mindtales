# Generated by Django 4.1.3 on 2022-11-16 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0003_remove_menu_food_item_menufooditem_menu_food_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="date_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
