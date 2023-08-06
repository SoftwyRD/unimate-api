# Generated by Django 4.1.10 on 2023-08-05 21:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("code", models.CharField(max_length=7, unique=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "credits",
                    models.IntegerField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_lab", models.BooleanField(default=False)),
            ],
        ),
    ]