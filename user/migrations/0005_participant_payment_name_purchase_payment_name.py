# Generated by Django 5.0 on 2024-01-23 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_user_social_provider_user_social_uid"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="payment_name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="purchase",
            name="payment_name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
