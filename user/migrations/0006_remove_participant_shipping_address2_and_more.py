# Generated by Django 5.0 on 2024-01-23 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0005_participant_payment_name_purchase_payment_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="participant",
            name="shipping_address2",
        ),
        migrations.RemoveField(
            model_name="purchase",
            name="shipping_address2",
        ),
        migrations.AlterField(
            model_name="participant",
            name="shipping_address1",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="purchase",
            name="shipping_address1",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
