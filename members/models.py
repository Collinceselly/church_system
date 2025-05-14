from django.db import models
from django.urls import reverse
import random
from django.contrib.auth.models import User

class Members(models.Model):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    marital_status_choices = [
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Widow/Widower', 'Widow/Widower'),
        ('Separated', 'Separated'),
        ('Divorced', 'Divorced'),
    ]
    membership_choices = [
        ('Transfer', 'Transfer'),
        ('Baptism', 'Baptism'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    marital_status = models.CharField(max_length=20, choices=marital_status_choices)
    membership_by = models.CharField(max_length=10, choices=membership_choices)
    occupation = models.CharField(max_length=50)
    residence_address = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=6, unique=True, editable=False, null=True)

    
    @staticmethod
    def generate_unique_id():
        while True:
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            if not Members.objects.filter(unique_id=unique_id).exists():
                return unique_id

    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = Members.generate_unique_id()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Members'

    def __str__(self):
        return self.first_name
    
    def get_absolute_url(self):
        return reverse('member_more_detail', kwargs={'pk':self.pk})
