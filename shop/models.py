from django.contrib.auth import get_user_model
from django.db import models


class Product(models.Model):
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='product/image/%Y/%m/%d')
    # link to the creator's product. This could be anything digital (ex: pdf, video, notion page)
    link = models.URLField()
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
