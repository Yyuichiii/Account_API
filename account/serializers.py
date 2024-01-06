from rest_framework import serializers
from .models import MyUser

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