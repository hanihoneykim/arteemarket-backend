import uuid
from django.db import models
from config.utils import compress_image, upload_path
from common.models import CommonModel


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name


class SaleItem(CommonModel):
    CATEGORY_CHOICES = [
        ("idol", "아이돌"),
        ("stationery", "문구"),
        ("accessory", "악세사리"),
        ("food", "푸드"),
        ("interior", "인테리어"),
        ("pet", "반려동물"),
        ("etc", "기타"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=False)
    creator = models.ForeignKey(
        "user.User", null=True, related_name="sales_items", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=upload_path)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True
    )
    bank_name = models.CharField(max_length=20, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_account_owner = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk and self.image:
            try:
                original = SaleItem.objects.get(pk=self.pk)
                if original.image != self.image:
                    self.image = compress_image(self.image, size=(500, 500))
            except SaleItem.DoesNotExist:
                self.image = compress_image(self.image, size=(500, 500))
            except:
                pass
        super().save(*args, **kwargs)


class FundingItem(CommonModel):
    CATEGORY_CHOICES = [
        ("idol", "아이돌"),
        ("stationery", "문구"),
        ("accessory", "악세사리"),
        ("food", "푸드"),
        ("interior", "인테리어"),
        ("pet", "반려동물"),
        ("etc", "기타"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=False)
    creator = models.ForeignKey(
        "user.User", null=True, related_name="funding_items", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    goal_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="목표 금액"
    )
    end_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_path)
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True
    )
    bank_name = models.CharField(max_length=20, null=True, blank=True)
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)
    bank_account_owner = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk and self.image:
            try:
                original = SaleItem.objects.get(pk=self.pk)
                if original.image != self.image:
                    self.image = compress_image(self.image, size=(500, 500))
            except SaleItem.DoesNotExist:
                self.image = compress_image(self.image, size=(500, 500))
            except:
                pass
        super().save(*args, **kwargs)


class MainPageSlideBanner(models.Model):
    image = models.ImageField(upload_to=upload_path, null=True, blank=True)


class Notice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True)
    title = models.CharField(max_length=120, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True)
    title = models.CharField(max_length=120, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.title
