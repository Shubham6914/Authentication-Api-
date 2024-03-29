from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendResetEmailSerializer,UserResetPasswordSerializer

from django.contrib.auth import authenticate
from . renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Genertae Token manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistration(APIView):
   renderer_classes = [UserRenderer] # this is my custom render class for error field 
   def post(self,request,format=None):
      serializer = UserRegistrationSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         user = serializer.save()
         token = get_tokens_for_user(user) 
         return Response({"token":token,"msg":"Registered Successfully..!"},
         status = status.HTTP_201_CREATED)
      # print(serializer.errors) this will display the ErrorDetail in console during bad request 
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
   
class UserLogin(APIView):
   renderer_classes = [UserRenderer]
   def post(self,request,format=None):
      serializer = UserLoginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         email = serializer.data.get('email')
         password = serializer.data.get('password')
         user = authenticate(email=email,password=password)
         if user is not None: 
            token = get_tokens_for_user(user)
            return Response({"token":token,"msg":"Login Successfully..!"},
            status = status.HTTP_200_OK)
         else:
            return Response({'errors':{'non_field_errors':['email or password is not valid']}},
                            status=status.HTTP_404_NOT_FOUND)
            
      
class UserProfileView(APIView):
   renderer_classes = [UserRenderer]
   
   # this permission class will check user for authentication using token 
   permission_classes=[IsAuthenticated]
   def get(self,request,format=None):
      serializer = UserProfileSerializer(request.user)
      return Response(serializer.data,status=status.HTTP_200_OK)
      
   
class UserChangePasswordView(APIView):
   renderer_classes = [UserRenderer]
   permission_classes=[IsAuthenticated]
   def post(self,request,format=None):
      serializer = UserChangePasswordSerializer(data=request.data,
                        context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Changed Successfully..!'},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
      
      
class SendResetEmailView(APIView):
   renderer_classes = [UserRenderer]
   def post(self,request,format=None):
      serializer = SendResetEmailSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Reset link sent. Please check your Email.!'},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
      

class UserResetPasswordView(APIView):
   renderer_classes = [UserRenderer]
   def post(self,request,uid,token,format=None):
      serializer = UserResetPasswordSerializer(data=request.data,
                  context={'uid':uid,'token':token})
      if serializer.is_valid(raise_exception=True):
         return Response({"msg":"Password Reset Successfully..!"},status=status.HTTP_200_OK)
      else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
         