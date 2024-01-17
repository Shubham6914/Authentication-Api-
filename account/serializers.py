
from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
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
            raise serializers.ValidationError("Password and confirmed password does't match")

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
            raise serializers.ValidationError("Password and confirmed password does't match")
        user.set_password(password)
        user.save()
        return attrs
    

class SendResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        fields = ['email']
        
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('User Id:',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token:',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link:',link)
            
            # send email
            body = "Click Following Link To Reset Your Password" + link
            data = {
                'subject' : 'Reset Your Password',
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)
            return attrs 
            
        else:
            raise serializers.ValidationError('You are not a Registered User ')
        



class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        try:
            # getting data from view
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and confirmed password doesn't match")
            # decoding uid to bytes and then convertinfg to str like 1,2,3
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id =id)
            # validating token id match then set password else raise validation error 
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not valid or Expired')
                