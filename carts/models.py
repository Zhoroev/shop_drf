from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    product = models.ManyToManyField(Product, through='ProductCart', related_name='carts')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'Корзинка пользователя {self.owner.username}'


# Создает автоматически корзину, когда создается user с UserType.PERSONAL_CABINET
@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created and instance.user_type == User.UserType.PERSONAL_CABINET:
        Cart.objects.create(owner=instance)


class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='product_cart')
    amount = models.IntegerField(default=1)