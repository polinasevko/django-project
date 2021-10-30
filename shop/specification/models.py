from django.db import models


class CategoryFeature(models.Model):
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=100)
    feature_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category.name} | {self.feature_type}"


class Validator(models.Model):
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    key = models.ForeignKey(CategoryFeature, on_delete=models.CASCADE)
    valid_value = models.CharField(max_length=100)

    def __str__(self):
        return f"Category {self.category.name} " \
               f"| Specification {self.key.feature_type}" \
               f"| Valud value {self.valid_value}"


class ProductFeature(models.Model):
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Product {self.product.title} | Specification {self.spec.feature_type}" \
               f" - {self.value}"
