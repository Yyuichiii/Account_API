from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializers,LoginSerializers,UserProfileSerializer,PasswordChangeSerializer,emailserializer,password_reset_serializers
from rest_framework_simplejwt.tokens import RefreshToken


# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):

    def post(self,request,format=None):
        serializer=UserRegistrationSerializers(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response({'msg':'Registration Page'})
    


class LoginView(APIView):

    def post(self,request,format=None):
        serializer=LoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                login(request,user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
        return Response({'msg':'Not login'},status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class passchange(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        serializer=PasswordChangeSerializer(data=request.data,context={'request': request.user})
        if serializer.is_valid(raise_exception=True):

            return Response({'msg':'Password Changed'},status=status.HTTP_200_OK)
        

class emailview(APIView):
    def post(self,request,format=None):
        serializer=emailserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            return Response({'msg':'Email has been send'},status=status.HTTP_200_OK)
        

class reset_password_view(APIView):
    def post(self,request,uid,token,format=None):
        serializer=password_reset_serializers(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):

            return Response({'msg':'Password Changed via Email'},status=status.HTTP_200_OK)