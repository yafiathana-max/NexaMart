from django.contrib import admin
from .models import Product, Category, Review, Coupon

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "original_price",
        "discount",
        "stock",
        "sold"
    )

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Coupon)