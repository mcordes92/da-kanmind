from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from auth_app.models import Profile

# Serializer for user registration with full name and password validation
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
        # Ensure email uniqueness across all users
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def validate_fullname(self, value):
        # Generate username slug from full name and check for duplicates
        slug = slugify(value)
        if User.objects.filter(username=slug).exists():
            raise serializers.ValidationError('A user with a similar name already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        # Verify that both password fields match
        if pw != repeated_pw:
            raise serializers.ValidationError("Passwords do not match")
        
        # Create username from slugified full name
        fullname = self.validated_data.pop('fullname')
        username_slug = slugify(fullname)

        user = User(email=self.validated_data['email'],
                    username=username_slug)
        user.set_password(pw)
        user.save()
        Profile.objects.create(user=user, full_name=fullname)
        return user
    
# Serializer for user login with email and password authentication
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        # Check if user with this email exists
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return value
    
    def get(self):
        email = self.validated_data['email']
        pw = self.validated_data['password']

        user = User.objects.get(email=email)

        # Verify password matches the hashed password in database
        if not user.check_password(pw):
            raise serializers.ValidationError({"email": email, "password": "Incorrect password"})
    
        return user