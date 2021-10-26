from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    details = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Product: {self.category.name} - {self.title}"

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number_of_item = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Cart with product: {self.product.title}"

    def save(self, *args, **kwargs):
        self.total_price = self.number_of_item * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_number = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonimous = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart: {self.id}"


class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_INPROGRESS = "ii_progress"
    STATUS_READY = "is_ready"
    STATUS_COMPLETED = "completed"

    BUYING_SELF = "self"
    BUYING_DELIVERY = "delivery"

    STATUS_CHOICES = (
        (STATUS_NEW, "New order"),
        (STATUS_INPROGRESS, "Order in progress"),
        (STATUS_READY, "Order is ready"),
        (STATUS_COMPLETED, "Order is completed"),
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_SELF, "Self-delivery"),
        (BUYING_DELIVERY, "Delivery"),
    )

    customer = models.ForeignKey('Customer', related_name='related_orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=9, default='+375')
    address = models.CharField(max_length=1024)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, choices=BUYING_TYPE_CHOICES, default=BUYING_DELIVERY)
    creation_date = models.DateTimeField(auto_now=True)
    order_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=9, null=True, blank=True)
    orders = models.ManyToManyField(Order, related_name='related_customer')

    def __str__(self):
        return f"Customer: {self.user}"
