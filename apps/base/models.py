from django.db import models
from apps.abstract.base_model import CreatedUpdatedAbstractModel
from django.core.validators import MinValueValidator, MaxValueValidator



class Banner(CreatedUpdatedAbstractModel):
   title = models.CharField(max_length=255,blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   first_image = models.ImageField(upload_to="banner/", blank=True, null=True)
   second_image= models.ImageField(upload_to="banner/", blank=True, null=True)
   video = models.FileField(upload_to="banner/", blank=True, null=True)

   def __str__(self):
       return str(self.title or f"Banner {self.id}")


   class Meta:
       ordering = ("-created_at",)


class Product(CreatedUpdatedAbstractModel):
   name = models.CharField(max_length=255,blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   image = models.ImageField(upload_to="users/", blank=True, null=True)
   category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
   rate = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(1),MaxValueValidator(5)])
   is_available = models.BooleanField(default=False)


   def __str__(self):
       return str(self.name or f"Product {self.id}")


   class Meta:
       ordering = ("-created_at",)




class Category(CreatedUpdatedAbstractModel):
   name = models.CharField(max_length=255,blank=True, null=True)
   image = models.ImageField(upload_to="users/", blank=True, null=True)


   def __str__(self):
       return str(self.name or f"Category {self.id}")


   class Meta:
       ordering = ("-created_at",)



class Sponsorship(CreatedUpdatedAbstractModel):
   image = models.ImageField(upload_to="sponsorship/", blank=True, null=True)


   class Meta:
       ordering = ("-created_at",)


class Message(CreatedUpdatedAbstractModel):
   full_name = models.CharField(max_length=255, blank=True, null=True)
   email = models.EmailField(max_length=255, blank=True, null=True)
   phone_number = models.CharField(max_length=255, blank=True, null=True)
   message = models.TextField(blank=True, null=True)


   class Meta:
       ordering = ("-created_at",)



class AboutUs(CreatedUpdatedAbstractModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="aboutus/", blank=True, null=True)
    employer_image = models.ImageField(upload_to="aboutus/", blank=True, null=True)
    statistics = models.ManyToManyField("Statistics", blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

class Statistics(CreatedUpdatedAbstractModel):
   name = models.CharField(max_length=255, blank=True, null=True)
   number = models.IntegerField(blank=True, null=True)

   class Meta:
       ordering = ("-created_at",)




class Order(CreatedUpdatedAbstractModel):
   full_name = models.CharField(max_length=255, blank=True, null=True)
   email = models.EmailField(max_length=255, blank=True, null=True)
   phone_number = models.CharField(max_length=255, blank=True, null=True)
   address = models.CharField(max_length=255, blank=True, null=True)
   description = models.TextField(blank=True, null=True)
   total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


   class Meta:
       ordering = ("-created_at",)




class OrderItem(CreatedUpdatedAbstractModel):
   order = models.ForeignKey("Order", on_delete=models.CASCADE, blank=True, null=True,related_name="items")
   product = models.ForeignKey("Product", on_delete=models.SET_NULL, blank=True, null=True)
   quantity = models.PositiveIntegerField(blank=True, null=True)


   def __str__(self):
       return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'}"



















































