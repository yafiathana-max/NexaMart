from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.IntegerField(default=0)

    sold = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)  
      
    def __str__(self):
        return self.name

class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars"


class Coupon(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    discount = models.IntegerField(
        help_text="Discount Percentage"
    )

    def __str__(self):
        return self.code