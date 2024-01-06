from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,status
from .models import MyUser
from .serializers import UserRegistrationSerializers

class UserRegistrationView(APIView):

    def post(self,request,format=None):
        serializer=UserRegistrationSerializers(data=request.data)
        print("Data :",request.data)
        print("Serializer :",serializer)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            print("user",user)
            return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response({'msg':'Registration Page'})