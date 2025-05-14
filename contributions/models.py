from django.db import models
from members.models import Members

class Contribution(models.Model):
    PAYMENT_MODES = (
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('mpesa', 'M-Pesa'),
    )
    
    member = models.ForeignKey(Members, on_delete=models.CASCADE, related_name='contributions')
    date = models.DateField()
    mode_of_payment = models.CharField(max_length=10, choices=PAYMENT_MODES)
    reference_code = models.CharField(max_length=50, blank=True, null=True)
    categories = models.JSONField(default=dict, blank=True, null=True)  # Store category-amount pairs as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.date}"