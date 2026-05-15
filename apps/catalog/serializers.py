from datetime import date
from django.utils import timezone
from rest_framework import serializers
from apps.catalog.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "brand", "model", "price", "release_date"]

    def validate_brand(self, value: str) -> str:
        if len(value) > 50:
            raise serializers.ValidationError(
                "Brand length cannot exceed 50 characters."
            )
        return value

    def validate_model(self, value: str) -> str:
        if len(value) > 25:
            raise serializers.ValidationError(
                "Model length cannot exceed 25 characters."
            )
        return value

    def validate_release_date(self, value: date) -> date:
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Release date cannot be in the future."
            )
        return value
