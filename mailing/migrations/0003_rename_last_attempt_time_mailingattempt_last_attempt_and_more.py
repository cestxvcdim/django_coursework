# Generated by Django 5.2 on 2025-04-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_client_user"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mailingattempt",
            old_name="last_attempt_time",
            new_name="last_attempt",
        ),
        migrations.AddField(
            model_name="mailing",
            name="title",
            field=models.CharField(
                default="Без названия", max_length=100, verbose_name="название рассылки"
            ),
        ),
    ]
