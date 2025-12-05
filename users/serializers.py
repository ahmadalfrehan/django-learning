from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validation_data):
        user = User.objects.create_user(**validation_data)
        return user
