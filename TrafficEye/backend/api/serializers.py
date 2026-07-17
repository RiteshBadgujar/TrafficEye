from rest_framework import serializers


class ViolationSerializer(serializers.Serializer):

    vehicle_number = serializers.CharField()

    owner_name = serializers.CharField()

    violation_type = serializers.CharField()

    location = serializers.CharField()

    officer_name = serializers.CharField()

    fine_amount = serializers.IntegerField()

    status = serializers.CharField()

    date = serializers.CharField()