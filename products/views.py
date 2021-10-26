from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from carts.serializers import CartSerializer
from carts.models import ProductCart
from products.serializers import ProductSerializer, AmountSerializer, RatingSerializer
from products.models import Product, Rating


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ]

    @action(permission_classes=[IsAuthenticated, ],
            methods=['post', 'delete', ], detail=True,
            serializer_class=AmountSerializer)
    def cart(self, request, *args, **kwargs):
        cart = request.user.cart
        product = self.get_object()

        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_amount = serializer.validated_data.get('amount')

        if request.method == 'POST':

            if requested_amount > product.amount:
                return Response({'error': 'Requested amount is larger than product amount'},
                                status=status.HTTP_400_BAD_REQUEST)

            product.amount -= requested_amount
            product.save()

            cart_product, created = ProductCart.objects.get_or_create(
                cart=cart,
                product=product,
            )
            if created:
                cart_product.amount += requested_amount
            cart_product.save()

            return Response({'success': True})

        elif request.method == 'DELETE':

            if ProductCart.objects.filter(cart=cart, product=product).exists():
                cart_product = ProductCart.objects.get(product=product, cart=cart)

                if requested_amount > cart_product.amount:
                    return Response({'error': 'Requested amount is larger than product amount'},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif requested_amount == cart_product.amount:
                    cart_product.delete()
                    return Response({'success': True})

                cart_product.amount -= requested_amount
                cart_product.save()
                return Response({'success': True})

            return Response({'error': 'Current cart does not contain this product'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(permission_classes=[IsAuthenticated, ],
            methods=['post', ], detail=True,)
    def rating(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating, created = Rating.objects.get_or_create(product=product, author=request.user,
                                              defaults={'value': serializer.validated_data['value']})

        if not created:
            rating.value = serializer.validated_data['value']
            rating.save()
        serializer = self.get_serializer(instance=product)
        return Response(serializer.data)




