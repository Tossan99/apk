from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
#from cloudinary.models import CloudinaryField

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Beverage(models.Model):
    """
    Model for beverages
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    #image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    volume = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)]) #Volume in ml
    price = models.DecimalField(max_digits=7, decimal_places=2) #Price in sek
    percentage = models.DecimalField(max_digits=4, decimal_places=2) #Alcohol percentage
    apk = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False) #Price in sek

    def __str__(self):
        return self.name
    
    def _calculate_apk(self):
        """
        Calculates the beverage apk, how many ml of 40% alcoholic liquid for each sek
        """
        apk = ((self.percentage / 100) * self.volume) / self.price
        return round(apk, 2)
    
    def _calculate_price_per_unit(self):
        """
        Calculate price_per_unit in sek
        One unit is set to 40ml 40% alcohol
        """
        x = (((5.00 / 100) * 330) / 0.4)
        price_per_unit = 9.00 / ( x / 40)
        return round(price_per_unit, 2)
        

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the apk and price_per_unit.
        """
        if not self.apk:
            self.apk = self._calculate_apk()
        if not self.price_per_unit:
            self.price_per_unit = self._calculate_price_per_unit()
        super().save(*args, **kwargs)