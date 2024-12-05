from rest_framework import serializers  #type:ignore
from products.models import Product
from users.models import Profile 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    seller = ProfileSerializer(many=False)
    class Meta:
        model = Product
        fields = "__all__"