from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from carts.serializers import CartSerializer
from carts.models import Cart
from orders.models import Order
import datetime


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # @action(methods=['post', ], detail=True)
    # def buy(self, request, *args, **kwargs):
    #     cart = request.user.cart
    #     product_list = f''
    #     total_amount = 0
    #     for product in cart.product:
    #         product_list += f'{product.name}, '
    #         total_amount += product.price
    #
    #     estimated_delivery_date = datetime.datetime.today() + datetime.timedelta(days=15)
    #     Order.object.create(cart=cart,
    #                         product_list=product_list,
    #                         total_amount=total_amount,
    #                         estimated_delivery_date=estimated_delivery_date)
    #
    #     serializer = OrderSerializer()
    #     return Response(serializer.data)