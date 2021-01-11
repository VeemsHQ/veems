from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CustomModelSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if self.partial and not validated_data:
            raise ValidationError('Invalid payload')
        return super().update(instance=instance, validated_data=validated_data)
