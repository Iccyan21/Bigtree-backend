# Generated by Django 4.1.7 on 2023-03-14 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_user_name"),
        ("timeline", "0014_alter_post_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="timeline_posts",
                to="accounts.user",
                to_field="name",
                unique=True,
            ),
        ),
    ]
