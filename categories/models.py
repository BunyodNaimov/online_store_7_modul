from random import randint

from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def my_slugify(value):
    return value.replace(' ', '-')


class Category(models.Model):
    name = models.CharField(_("Category name"), max_length=100, )
    slug = AutoSlugField(populate_from='name',
                         unique_with=['name'],
                         slugify=my_slugify)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='sub_category')

    def get_absolute_url(self):
        """ Создание уникального url категории по slug
        """
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True, unique=True)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)

    @staticmethod
    def get_all_brands():
        return Brand.objects.all()

    def __str__(self):
        return str(self.name)
