from django.contrib import admin
from .models import (
    Banner,
    Sponsorship,
    Message,
    Product,
    Category
)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id","title","description")
    list_filter = ("title","description")

@admin.register(Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ("id","image")
    list_filter = ("id",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id","full_name","email","message","phone_number")
    list_filter = ("id","full_name","email","phone_number")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","price","image","category","rate")
    list_filter = ("id","name","price","category","rate")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","image")
    list_filter = ("id","name")