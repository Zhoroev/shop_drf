from rest_framework import serializers
from django.db import models
from products.models import Product, Rating


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'amount', 'price', 'category', 'rating']


class RatingSerializer(serializers.Serializer):
    value = serializers.IntegerField()


class AmountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
