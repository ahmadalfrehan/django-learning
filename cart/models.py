from django.db import models

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)

    def total(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    varient = models.ForeignKey(
        'products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.variant.price * self.quantity
