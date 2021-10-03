from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = models.ImageField(upload_to='static/avatar/%Y/%m', default=None)

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
    city = models.ForeignKey("City", on_delete=models.SET_NULL, related_name="tours", null=True)
    datetime = models.DateTimeField(null=True)
    duaration = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField(default=None, null=True)
    stock = models.CharField(max_length=500, null=True)
    available = models.BooleanField(default=True)

class Seat(ItemBase):
    price = models.CharField(max_length=9999, null=True)
    tour = models.ForeignKey("Tour", related_name="seats", on_delete=models.CASCADE, null=True)

class Tag(ItemBase):
    tour = models.ManyToManyField("Tour", related_name="tags", blank=True)

class Comment(ItemBase):
    class Meta:
        ordering = ['-id']

    rating = models.IntegerField(null=True, blank=True)
    tour = models.ForeignKey("Tour", related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="comments", on_delete=models.CASCADE)

class Ticket(models.Model):
    tour = models.ForeignKey("Tour", related_name="tickets", on_delete=models.CASCADE)
    user = models.ForeignKey("User", related_name="tickets", on_delete=models.CASCADE)
    price = models.CharField(max_length=20, null=True)
    quantity = models.CharField(max_length=500, null=True)
    created_day = models.DateTimeField(auto_now_add=True)











