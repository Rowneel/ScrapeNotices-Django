from django.db import models

# Create your models here.
class Notice(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    pdf = models.CharField(max_length=400)

    def __str__(self):
        return self.title
    