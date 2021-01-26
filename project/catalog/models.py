from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)

    def __str__(self):
        
        return '{0} ({1})'.format (self.name, self.price)
