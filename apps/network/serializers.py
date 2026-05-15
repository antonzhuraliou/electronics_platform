from rest_framework import serializers
from apps.network.models import Outlet, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "phone", "email"]


class OutletSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = Outlet
        fields = [
            "id",
            "outlet_type",
            "name",
            "country",
            "city",
            "street",
            "house_number",
            "daily_revenue",
            "employees",
        ]

        read_only_fields = ["daily_revenue"]
        extra_kwargs = {
            "name": {"max_length": 50},
        }


class OutletAboveAverageSerializer(serializers.ModelSerializer):
    """Lightweight serializer for stats endpoint."""

    class Meta:
        model = Outlet
        fields = ["id", "name", "city", "daily_revenue"]
