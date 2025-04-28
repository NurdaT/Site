from django.contrib import admin
from .models import Burger


@admin.register(Burger)
class BurgerAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    ordering = ("-created_at",)

    fieldsets = (
        ("Main Info", {
            "fields": ("name", "price", "description"),
        }),
        ("Additional Info", {
            "fields": ("image",),
        }),
    )