from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    pass

class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255, null=False)
    created_day = models.DateTimeField(auto_now_add=True)
    upload_day = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class City(ItemBase):
    pass

class Tour(ItemBase):
    image = models.ImageField(upload_to='img/%Y/%m', default=None, null=True, blank=True)
    city = models.ForeignKey("City", on_delete=models.SET_NULL, related_name="tour", null=True)
    datetime = models.DateTimeField(null=True)
    duaration = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField(default=None, null=True)
    stock = models.CharField(max_length=500, null=True)
    available = models.BooleanField(default=True)

class Seat(ItemBase):
    price = models.CharField(max_length=9999, null=True)
    tour = models.ForeignKey("Tour", related_name="seat", on_delete=models.CASCADE, null=True)

class Khachhang(ItemBase):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default=None, null=True)
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    sdt = models.CharField(max_length=20, null=True, default=True)
    gmail = models.CharField(max_length=255, null=True, default=True)
    money = models.CharField(max_length=9999, null=True, default=True)
    tour = models.ManyToManyField("Tour", related_name="khachhang")
    seat = models.ManyToManyField("Seat", related_name="khachhang")












