# Generated by Django 4.1.7 on 2023-03-14 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=32, unique=True),
        ),
    ]