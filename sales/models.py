from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(max_length=50, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    date_of_sale = models.DateField()
    payment_method = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['date_of_sale']),
            models.Index(fields=['region']),
        ]
    
    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'order_items'
        unique_together = ('order', 'product')
    
    @property
    def total_price(self):
        return self.quantity * self.unit_price * (1 - self.discount)
    
    def __str__(self):
        return f"{self.order.order_id} - {self.product.name}"