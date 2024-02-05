from django.contrib import admin
from .models import Category, MainPageSlideBanner, FundingItem, SaleItem, Notice, Event


class FundingItemAdmin(admin.ModelAdmin):
    search_fields = ["title"]


admin.site.register(Category)
admin.site.register(MainPageSlideBanner)
admin.site.register(FundingItem, FundingItemAdmin)
admin.site.register(SaleItem)
admin.site.register(Notice)
admin.site.register(Event)
