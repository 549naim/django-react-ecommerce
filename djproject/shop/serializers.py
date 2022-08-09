from pyexpat import model
from rest_framework import serializers
from . models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields ="__all__"
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ="__all__"
        depth = 1
User=get_user_model()        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =("id","username","password","first_name","last_name","email")
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        return user    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields ="__all__"
        depth = 1
        read_only_fields = ["prouser"]
    def validate(self,attrs):
        attrs['prouser'] =self.context['request'].user
        return attrs
    def to_representation(self,instance):
        response=super().to_representation(instance)
        response['prouser'] =UserSerializer(instance.prouser).data
        return response    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields ="__all__"

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields ="__all__"
        depth = 1        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields ="__all__"
        depth = 3        