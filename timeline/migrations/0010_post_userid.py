# Generated by Django 4.1.7 on 2023-03-14 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_password"),
        ("timeline", "0009_remove_post_userid"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="UserID",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="UserID+",
                to="accounts.user",
            ),
            preserve_default=False,
        ),
    ]
