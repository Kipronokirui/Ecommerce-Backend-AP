from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class Order(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    # order_code = models.CharField(max_length=50, unique=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    ordered_on = models.DateTimeField(auto_now_add=True, editable=False)
    delivered_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order {self.order.title}"
    
    class Meta:
        # Add a unique constraint to ensure a product can't be added to an order more than once
        unique_together = ('order', 'product')