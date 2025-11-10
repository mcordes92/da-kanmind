from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import Profile
from django.utils.text import slugify

class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=100, write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', "fullname"]
        read_only_fields = ['username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_fullname(self, value):
        slug = slugify(value)
        print(f"Generated slug: {slug}")
        if User.objects.filter(username=slug).exists():
            raise serializers.ValidationError('A user with a similar name already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError("Passwords do not match")
        
        fullname = self.validated_data.pop('fullname')
        username_slug = slugify(fullname)

        user = User(email=self.validated_data['email'],
                    username=username_slug)
        user.set_password(pw)
        user.save()
        Profile.objects.create(user=user, full_name=fullname)
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return value
    
    def get(self):
        email = self.validated_data['email']
        pw = self.validated_data['password']

        user = User.objects.get(email=email)

        if not user.check_password(pw):
            raise serializers.ValidationError("Incorrect password")
    
        return user