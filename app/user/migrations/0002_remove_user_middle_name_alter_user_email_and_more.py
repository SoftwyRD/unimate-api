# Generated by Django 4.1.10 on 2023-08-07 01:38

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="middle_name",
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with that email already exists."},
                help_text="Required. 255 characters or fewer.",
                max_length=255,
                unique=True,
                verbose_name="email",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                help_text="Required. 50 characters or fewer.",
                max_length=50,
                verbose_name="first name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(
                editable=False,
                help_text="Required. Autogenerated. Non editable.",
                primary_key=True,
                serialize=False,
                unique=True,
                verbose_name="id",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                help_text="Required. 50 characters or fewer.",
                max_length=50,
                verbose_name="last name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 20 characters or fewer.",
                max_length=20,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]
