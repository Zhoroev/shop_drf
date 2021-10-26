from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'products_list',
                  'total_amount', 'estimated_delivery_date',
                  'status',]
