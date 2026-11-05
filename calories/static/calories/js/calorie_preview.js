document.addEventListener("DOMContentLoaded", () => {
    const quantityInput = document.getElementById("id_quantity_grams");
    const caloriesInput = document.getElementById("id_calories_per_100g");
    const preview = document.getElementById("calorie-preview");
    const previewValue = document.getElementById("calorie-preview-value");

    if (!quantityInput || !caloriesInput || !preview || !previewValue) {
        return;
    }

    function updateCaloriePreview() {
        const quantity = quantityInput.valueAsNumber;
        const caloriesPer100g = caloriesInput.valueAsNumber;

        if (
            !quantityInput.validity.valid ||
            !caloriesInput.validity.valid ||
            !Number.isFinite(quantity) ||
            !Number.isFinite(caloriesPer100g) ||
            quantity <= 0 ||
            caloriesPer100g < 0
        ) {
            previewValue.textContent = "—";
            return;
        }

        const totalCalories = quantity * caloriesPer100g / 100;
        previewValue.textContent = totalCalories.toFixed(2);
    }

    quantityInput.addEventListener("input", updateCaloriePreview);
    caloriesInput.addEventListener("input", updateCaloriePreview);
    preview.hidden = false;
    updateCaloriePreview();
});
