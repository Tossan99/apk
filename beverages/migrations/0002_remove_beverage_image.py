# Generated by Django 4.2.10 on 2024-02-29 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("beverages", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="beverage",
            name="image",
        ),
    ]
