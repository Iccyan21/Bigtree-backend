# Generated by Django 4.1.7 on 2023-03-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(max_length=32, unique=True, verbose_name="name"),
        ),
    ]
