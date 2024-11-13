from django.db import models

category_item=(
    ("buf","buf"),
    ('chicken',"chicken"),
    ("veg","veg")
    
)
# Create your models here.
class Momo(models.Model):
    title=models.CharField(max_length=200)
    category=models.CharField(choices=category_item,max_length=200)
    image=models.ImageField(upload_to='images')
    price=models.DecimalField(max_digits=8,decimal_places=2)
    
    def __str__(self):
        return self.title
