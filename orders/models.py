from django.db import models
from carts.models import Cart


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        SUCCESS = 'Successfully delivered'
        PENDING = 'Pending'
        CANCEL = 'Cancellation'

    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='orders',)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    products_list = models.TextField()
    total_amount = models.IntegerField()
    estimated_delivery_date = models.DateTimeField()
    status = models.CharField(max_length=50,
                              choices=OrderStatus.choices,
                              default=OrderStatus.PENDING)


