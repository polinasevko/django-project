from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, view_name):
    content_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'content_model': content_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args):
        products = []
        content_models = ContentType.objects.filter(model__in=args)
        for content_mod in content_models:
            model_products = content_mod.model_class()._base_manager.all().order_by('id')[:]
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    category_name_count_name = {
        'Guitars': 'guitarproduct__count',
        'Piano': 'pianoproduct__count',
        'Mics': 'micproduct__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_sidebar(self):
        models = get_models_for_count('guitarproduct', 'pianoproduct', 'micproduct')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(),
                 count=getattr(c, self.category_name_count_name[c.name])) for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    objects = CategoryManager()

    def __str__(self):
        return f"Category: {self.name}"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    details = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Product: {self.category.name} - {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


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
    weigth = models.DecimalField(decimal_places=1, max_digits=4)
    heigth = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()


# MIC
#
# sensitivity
# min_frequency
# max_frequency

class MicProduct(Product):
    sensitivity = models.PositiveSmallIntegerField()
    min_frequency = models.PositiveSmallIntegerField()
    max_frequency = models.PositiveSmallIntegerField()


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    number_of_item = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Cart with product: {self.content_object.title}"

    def save(self, *args, **kwargs):
        self.total_price = self.number_of_item * self.content_object.price
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

    def save(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('total_price'), models.Count('id'))
        print(cart_data)
        if cart_data['total_price__sum']:
            self.total_price = cart_data['total_price__sum']
        else:
            self.total_price = 0
        self.total_number = cart_data['id__count']
        return super().save()



# class Order(models.Model):
#     pass


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        return f"Customer: {self.user}"
