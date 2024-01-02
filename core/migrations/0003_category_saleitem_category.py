# Generated by Django 5.0 on 2023-12-28 10:23

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_saleitem_creator"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name="saleitem",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.category",
            ),
        ),
    ]