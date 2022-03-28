from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {"password": {"write_only":True}} # for write only not for accessing


    def create(self,validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user


#for password change
class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
