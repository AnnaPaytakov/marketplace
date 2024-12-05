from django.db import models                                                     #type:ignore

# Create your models here.

class Contact(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=15, null=True, blank=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    instagram = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.phone1
