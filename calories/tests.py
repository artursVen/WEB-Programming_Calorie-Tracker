from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import FoodEntry


class FoodEntryDeletionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="owner")
        cls.other_user = get_user_model().objects.create_user(username="other")
        cls.entry = FoodEntry.objects.create(
            user=cls.owner,
            name="Auzu pārslas",
            quantity_grams=Decimal("80"),
            calories_per_100g=Decimal("370"),
            meal_type=FoodEntry.MealType.BREAKFAST,
        )

    def setUp(self):
        self.client.force_login(self.owner)
        self.url = reverse("calories:delete_entry", args=[self.entry.pk])

    def test_confirmation_and_cancel_preserve_entry(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auzu pārslas")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, reverse("calories:dashboard"))
        self.client.get(reverse("calories:dashboard"))
        self.assertTrue(FoodEntry.objects.filter(pk=self.entry.pk).exists())

    def test_post_deletes_entry_and_updates_total(self):
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse("calories:dashboard"))
        self.assertFalse(FoodEntry.objects.filter(pk=self.entry.pk).exists())
        self.assertContains(response, "veiksmīgi dzēsts")
        self.assertEqual(response.context["total_calories"], Decimal("0.00"))

    def test_other_user_cannot_view_or_delete_entry(self):
        self.client.force_login(self.other_user)
        for method in (self.client.get, self.client.post):
            self.assertEqual(method(self.url).status_code, 404)
        self.assertTrue(FoodEntry.objects.filter(pk=self.entry.pk).exists())

    def test_anonymous_user_must_log_in(self):
        self.client.logout()
        for method in (self.client.get, self.client.post):
            self.assertRedirects(
                method(self.url),
                f"{reverse('login')}?next={self.url}",
            )
        self.assertTrue(FoodEntry.objects.filter(pk=self.entry.pk).exists())

    def test_missing_entry_returns_404(self):
        self.entry.delete()
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.post(self.url).status_code, 404)

    def test_csrf_token_is_required_for_deletion(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertTrue(FoodEntry.objects.filter(pk=self.entry.pk).exists())
        client.get(self.url)
        response = client.post(
            self.url,
            {"csrfmiddlewaretoken": client.cookies["csrftoken"].value},
        )
        self.assertRedirects(response, reverse("calories:dashboard"))
        self.assertFalse(FoodEntry.objects.filter(pk=self.entry.pk).exists())
