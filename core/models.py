import uuid
from django.db import models
from config.utils import compress_image, upload_path
from common.models import CommonModel
from user.models import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False)


class SaleItem(CommonModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=False)
    creator = models.ForeignKey(
        User, null=True, related_name="sales_items", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True, upload_to=upload_path)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

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
