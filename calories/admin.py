from django.contrib import admin

from .models import FoodEntry


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "quantity_grams",
        "calories_per_100g",
        "total_calories_display",
        "meal_type",
        "consumed_at",
    )

    list_filter = (
        "meal_type",
        "consumed_at",
    )

    search_fields = (
        "name",
        "user__username",
    )

    date_hierarchy = "consumed_at"
    ordering = ("-consumed_at",)
    list_select_related = ("user",)
    readonly_fields = ("created_at",)

    @admin.display(description="Kopā (kcal)")
    def total_calories_display(self, obj):
        return obj.total_calories
