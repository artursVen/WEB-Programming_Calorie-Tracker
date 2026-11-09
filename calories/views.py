from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FoodEntryForm
from .models import FoodEntry


@login_required
def dashboard(request):
    if request.method == "POST":
        form = FoodEntryForm(request.POST)

        if form.is_valid():
            food_entry = form.save(commit=False)
            food_entry.user = request.user
            food_entry.save()

            messages.success(
                request,
                "Pārtikas ieraksts veiksmīgi pievienots.",
            )

            return redirect("calories:dashboard")
    else:
        form = FoodEntryForm()

    today = timezone.localdate()

    food_entries = FoodEntry.objects.filter(
        user=request.user,
        consumed_at__date=today,
    )

    total_calories = sum(
        (entry.total_calories for entry in food_entries),
        Decimal("0.00"),
    )

    context = {
        "form": form,
        "food_entries": food_entries,
        "total_calories": total_calories,
        "today": today,
    }

    return render(
        request,
        "calories/dashboard.html",
        context,
    )


@login_required
def edit_food_entry(request, entry_id):
    food_entry = get_object_or_404(
        FoodEntry,
        id=entry_id,
        user=request.user,
    )

    if request.method == "POST":
        form = FoodEntryForm(
            request.POST,
            instance=food_entry,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Pārtikas ieraksts veiksmīgi atjaunināts.",
            )

            return redirect("calories:dashboard")

    else:
        form = FoodEntryForm(instance=food_entry)

    context = {
        "form": form,
        "food_entry": food_entry,
    }

    return render(
        request,
        "calories/edit_entry.html",
        context,
    )


@login_required
def delete_food_entry(request, entry_id):
    food_entry = get_object_or_404(
        FoodEntry,
        id=entry_id,
        user=request.user,
    )

    if request.method == "POST":
        entry_name = food_entry.name
        food_entry.delete()

        messages.success(
            request,
            f'Pārtikas ieraksts "{entry_name}" veiksmīgi dzēsts.',
        )

        return redirect("calories:dashboard")

    context = {
        "food_entry": food_entry,
    }

    return render(
        request,
        "calories/delete_entry.html",
        context,
    )
