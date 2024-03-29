# Generated by Django 5.0 on 2024-01-17 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_fundingitem_category_alter_saleitem_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fundingitem",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("idol", "아이돌"),
                    ("stationery", "문구"),
                    ("accessory", "악세사리"),
                    ("food", "푸드"),
                    ("interior", "인테리어"),
                    ("pet", "반려동물"),
                    ("etc", "기타"),
                ],
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="fundingitem",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="saleitem",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("idol", "아이돌"),
                    ("stationery", "문구"),
                    ("accessory", "악세사리"),
                    ("food", "푸드"),
                    ("interior", "인테리어"),
                    ("pet", "반려동물"),
                    ("etc", "기타"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
