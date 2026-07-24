from rest_framework import serializers


class ViolationSerializer(serializers.Serializer):

    vehicle_number = serializers.CharField(max_length=20)

    owner_name = serializers.CharField(max_length=100)

    violation_type = serializers.CharField(max_length=100)

    location = serializers.CharField(max_length=100)

    officer_name = serializers.CharField(max_length=100)

    fine_amount = serializers.IntegerField(min_value=0)

    status = serializers.ChoiceField(
        choices=["Pending", "Paid"]
    )

    date = serializers.DateField()