from django.db import models


class CategoryFeature(models.Model):
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.feature_type}"


class ProductFeature(models.Model):
    feature = models.ForeignKey(CategoryFeature, on_delete=models.CASCADE)
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Product {self.product.title} | Specification {self.feature.feature_type}" \
               f" - {self.value}"
