# Generated by Django 5.0 on 2024-09-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "avatar_name",
                    models.CharField(
                        error_messages={
                            "max_length": "name of the avatar you upload is too long"
                        },
                        max_length=100,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
