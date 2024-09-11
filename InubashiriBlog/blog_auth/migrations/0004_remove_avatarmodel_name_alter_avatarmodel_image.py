# Generated by Django 5.0 on 2024-09-10 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog_auth", "0003_avatarmodel_delete_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="avatarmodel",
            name="name",
        ),
        migrations.AlterField(
            model_name="avatarmodel",
            name="image",
            field=models.ImageField(upload_to="avatars/"),
        ),
    ]
