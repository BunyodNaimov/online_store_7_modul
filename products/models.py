from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from categories.models import Category, Brand


def get_path_product_image(instance, file):
    """ Построение пути к файлу image
    """
    return f'media/{instance.slug}/{file}'


class Product(models.Model):
    """ Модель товара
    """

    title = models.CharField('Название', max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.PROTECT, related_name='product_brand')
    image = models.ImageField('Изображение', upload_to=get_path_product_image, blank=True)
    count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    description = models.TextField('Описание', blank=True)
    price = models.FloatField('Цена')
    available = models.BooleanField('Наличие', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        slug = self.slug
        if self.__class__.objects.filter(slug=slug).exists():
            slug = f"{self.slug}-{self.id}"
        self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """ Создание уникального url товара по slug
        """
        return reverse('product', kwargs={'slug': self.slug})

    def __str__(self):
        print('title')
        return self.title


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="specifications")
    name = models.CharField(max_length=256, default="")
    value = models.CharField(max_length=256, default="")


class ProductImage(models.Model):
    name = models.CharField(max_length=128, null=False, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.FileField(upload_to=get_path_product_image)

    def src(self):
        return self.image

    def __str__(self):
        return f"/{self.image}"
