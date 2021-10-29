from django.db import models


class CategorySpec(models.Model):
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category.name} | {self.specification}"


class Validator(models.Model):
    category = models.ForeignKey('mainapp.Category', on_delete=models.CASCADE)
    key = models.ForeignKey(CategorySpec, on_delete=models.CASCADE)
    valid_value = models.CharField(max_length=100)

    def __str__(self):
        return f"Category {self.category.name} " \
               f"| Specification {self.key.specification}" \
               f"| Valud value {self.valid_value}"


class ProductSpec(models.Model):
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE)
    spec = models.ForeignKey(CategorySpec, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"Product {self.product.title} | Specification {self.spec.specification}" \
               f" - {self.value}"
