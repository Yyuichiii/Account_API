from rest_framework import serializers
from .models import MyUser
# Important for encoding and decoding
from django.utils.encoding import force_str,force_bytes,DjangoUnicodeDecodeError,smart_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class UserRegistrationSerializers(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=MyUser
        fields=['email','name','password','password2','tc']
        extra_kwargs={'password':{'write_only':True}}

    # Valdiate password and password 2
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        

        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password does'nt match")
        
        return attrs
    

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    


class LoginSerializers(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    password=serializers.CharField(style={'input_type':'password'})
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['email','name','tc','created_at']

class PasswordChangeSerializer(serializers.Serializer):
    password1=serializers.CharField(style={'input_type':'password'})
    password2=serializers.CharField(style={'input_type':'password'})

    def validate(self, attrs):
        password1=attrs.get('password1')
        password2=attrs.get('password2')
        user=self.context.get('request')
        print("user",user)

        if password1!=password2:
            raise serializers.ValidationError("Password and Confirm Password does'nt match")
        
        user.set_password(password1)
        user.save()
        return attrs


class emailserializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email=attrs.get('email')

        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link="http://127.0.0.1:8000/api/user/reset/"+uid+"/"+token+"/"
            print(link)
        else:
            raise serializers.ValidationError("User with the email does'nt exists")
        
        
        return attrs
    


class password_reset_serializers(serializers.Serializer):
    password1=serializers.CharField(style={'input_type':'password'})
    password2=serializers.CharField(style={'input_type':'password'})

    def validate(self, attrs):
        password1=attrs.get('password1')
        password2=attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        try:
            if password1!=password2:
                raise serializers.ValidationError("Password and Confirm Password does'nt match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not valid or expired")
            user.set_password(password1)
            user.save()
            return attrs
        except:
            raise serializers.ValidationError("Something Wrong Happened")