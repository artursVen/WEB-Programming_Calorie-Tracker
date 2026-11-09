from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class FoodEntry(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = "breakfast", "Brokastis"
        LUNCH = "lunch", "Pusdienas"
        DINNER = "dinner", "Vakariņas"
        SNACK = "snack", "Uzkoda"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="food_entries",
        verbose_name="Lietotājs",
    )

    name = models.CharField(
        max_length=120,
        verbose_name="Produkta nosaukums",
    )

    quantity_grams = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Daudzums gramos",
    )

    calories_per_100g = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name="Kalorijas uz 100g",
    )

    meal_type = models.CharField(
        max_length=20,
        choices=MealType.choices,
        verbose_name="Maltītes veids",
    )

    consumed_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Maltītes patērēšanas laiks",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Izveidošanas laiks",
    )

    @property
    def total_calories(self):
        result = self.quantity_grams * self.calories_per_100g / Decimal("100")
        return result.quantize(Decimal("0.01"))

    def __str__(self):
        return f"{self.name} - {self.total_calories} kcal"

    class Meta:
        ordering = ["-consumed_at", "-created_at"]
        verbose_name = "Pārtikas ieraksts"
        verbose_name_plural = "Pārtikas ieraksti"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity_grams__gt=0),
                name="food_quantity_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(calories_per_100g__gte=0),
                name="food_calories_gte_zero",
            ),
        ]
