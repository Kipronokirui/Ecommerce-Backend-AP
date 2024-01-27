from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

class ManufacturingCompany(models.Model):
    sub_category = models.ManyToManyField(SubCategory)
    title = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    category = models.ManyToManyField(Category)
    sub_category = models.ManyToManyField(SubCategory)
    manufacturer = models.ForeignKey(ManufacturingCompany, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_discounted = models.BooleanField(default=False)
    discounted_price = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    discount_end_date = models.DateTimeField(blank=True, null=True)
    is_flash_sale = models.BooleanField(default=False)
    flash_sale_price = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    flash_sale_end_date = models.DateTimeField(blank=True, null=True)
    cover_image = models.ImageField(blank=True, null=True)

    def clean(self):
        now = timezone.now()
        if self.is_discounted:
            if self.discounted_price is None:
                raise ValidationError("Please enter the new price of the discounted item.")
            else:
                if self.discounted_price >= self.price:
                    raise ValidationError("Discounted price must be less than the original price.")
            if self.discount_end_date is None:
                raise ValidationError("Discount end date must be provided for discounted products.")
            else:
                if self.discount_end_date <= now:
                    raise ValidationError("Discount end date must be in the future.")
        else:
            if self.discounted_price is not None:
                raise ValidationError("A non discounted item cannot have a discount price.")
            if self.discount_end_date is not None:
                raise ValidationError("A non discounted item cannot have an end of discount date.")
                
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False)

    def __str__(self):
        return f"Image added for {self.product.title}"

