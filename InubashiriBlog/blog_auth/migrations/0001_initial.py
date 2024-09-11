# Generated by Django 5.0 on 2024-09-07 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CaptchaModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("captcha", models.CharField(max_length=6)),
                ("create_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
