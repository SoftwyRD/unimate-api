# Generated by Django 4.1.10 on 2023-08-14 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("selection", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="selection",
            name="user",
            field=models.ForeignKey(
                help_text="Selection's owner.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="selection",
                related_query_name="selection",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="selection",
            unique_together={("name_slug", "user")},
        ),
    ]
