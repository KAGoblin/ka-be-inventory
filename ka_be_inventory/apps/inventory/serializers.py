from rest_framework import serializers


class ValidateProductAvailabilitySerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
