from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import PostModel


class UserLoginsSerializers(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone:
            raise ValidationError("phone is required")
        if not (attrs['phone'].startswith('09') and attrs['phone'].isnumeric()):
            raise ValidationError('Phone number is not valid')
        return attrs


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        if not (attrs['phone'].startswith('09') and attrs['phone'].isnumeric()):
            raise ValidationError('Phone number is not valid')
        if not (attrs["code"].isnumeric() and len(attrs["code"]) == 6):
            raise ValidationError("otp in not valid")
        return attrs


class PostSerializers(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=900)

    class Meta:
        model = PostModel
        fields = ['id', 'owner', 'title', 'slug', 'text', 'created', 'modified']
        read_only_fields = ['created', 'modified', 'id', 'owner', 'slug']
