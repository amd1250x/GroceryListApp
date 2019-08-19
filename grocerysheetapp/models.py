from django.db import models

# Create your models here.
class GroceryList(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    buyer = models.CharField(max_length=255)

    class Meta:
        ordering = ['date']
        def __unicode__(self):
            return self.name

class Person(models.Model):
    name = models.CharField(max_length=255)
    glist = models.ForeignKey(GroceryList, on_delete=models.CASCADE)
    cost = models.FloatField(default=0.00)

    def __str__(self):
        return(self.name)

class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    glist = models.ForeignKey(GroceryList, on_delete=models.CASCADE)
    people = models.ManyToManyField(Person, blank=True)

    def __str__(self):
        return(self.name)

