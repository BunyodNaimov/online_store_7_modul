from random import randint

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from categories.models import Category, Brand


class Product(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.PROTECT, related_name='product_brand')
    image = models.ImageField('Изображение', upload_to='products/', null=True, blank=True)
    count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # slug = self.slug
        # if self.__class__.objects.filter(slug=slug).exists():
        #     slug = f"{self.slug}-{self.id}"
        # self.slug = slug
        super().save(*args, **kwargs)

        self.slug = slugify(f'{self.name} {self.id}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class SpecificationAttribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    attribute = models.ForeignKey(SpecificationAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product} - {self.attribute}: {self.value}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', null=True)

    def __str__(self):
        return f'{self.product} - {self.image}'
