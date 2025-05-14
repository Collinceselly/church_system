from django.db import models
from members.models import Members


class Children(models.Model):
    GENDER_CHOICES = [
        ('Male','Male'),
        ('Female','Female'),
    ]
    
    father = models.ForeignKey(Members, on_delete=models.SET_NULL, null=True, blank=True, related_name='father_children')
    mother = models.ForeignKey(Members, on_delete=models.SET_NULL, null=True, blank=True, related_name='mother_children')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    

    def __str__(self):
        return f'{self.first_name} {self.middle_name}'
