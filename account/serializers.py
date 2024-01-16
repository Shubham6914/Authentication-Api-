
from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and confirmed password don't match")

        return data
    def create(self, validate_data):
         # Create the user without the password
         user = User.objects.create_user(**validate_data)
         return user



class UserLoginSerializer(serializers.ModelSerializer):
   email = serializers.EmailField(max_length=255)
   class Meta:
      model = User
      fields = ['email','password']
      
      
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email']
        
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user') # here we are getting user from context variable from view
        if password != password2:
            raise serializers.ValidationError("Password and confirmed password don't match")
        user.set_password(password)
        user.save()
        return attrs