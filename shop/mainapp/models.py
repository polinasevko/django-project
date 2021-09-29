from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return f"Category: {self.name}"


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Product: {self.category.name} - {self.title}"


# GUITAR
#
# type
# top_material
# nut_width
# scale_length

class GuitarProduct(Product):
    type = models.CharField(max_length=50, default="Classic")
    top_material = models.CharField(max_length=50)
    nut_width = models.DecimalField(decimal_places=1, max_digits=3)
    frets = models.PositiveSmallIntegerField(default=20)


# PIANO
#
# keys_number
# weigth
# heigth
# width

class PianoProduct(Product):
    keys_number = models.PositiveSmallIntegerField()
    weigth = models.DecimalField(decimal_places=1, max_digits=3)
    heigth = models.DecimalField(decimal_places=1, max_digits=3)
    width = models.DecimalField(decimal_places=1, max_digits=3)


# MIC
#
# sensitivity
# min_frequency
# max_frequency

class MicProduct(Product):
    sensitivity = models.PositiveSmallIntegerField()
    min_frequency = models.PositiveSmallIntegerField()
    max_frequency = models.PositiveSmallIntegerField()

    # def __str__(self):
    #     return f"Product: {self.category.name} - {self.title}"


class ProductInCart(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    obj_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'obj_id')
    number_of_item = models.PositiveIntegerField(default=1)
    total_sum = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Cart product: {self.product.title}"


class Cart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInCart, blank=True, related_name='related_cart')
    total_number = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Cart: {self.id()}"


class Order(models.Model):
    pass


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=9)

    def __str__(self):
        return f"Customer: {self.user.first_name} {self.user.last_name}"
