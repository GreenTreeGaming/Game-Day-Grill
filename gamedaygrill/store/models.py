from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.

PRODUCT_TYPES = (
    ('A', 'Appetizer'),
    ('MC', 'Main Course'),
    ('D', 'Dessert'),
    ('S', 'Side'),
    ('E', 'Extras'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type = models.CharField(max_length=2, choices=PRODUCT_TYPES, null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Reservation(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    party_size = models.IntegerField()
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=100, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    special_requests = models.TextField(max_length=500, null=True, blank=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, default='17:00:00')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for order in orderitems:
            shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address