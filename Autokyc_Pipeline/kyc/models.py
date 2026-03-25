from django.db import models
from accounts.models import Customer

class KYCSession(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVIEW', 'Manual Review'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    risk_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KYC-{self.id} - {self.status}"

class KYCAuditLog(models.Model):
    kyc_session = models.ForeignKey(KYCSession, on_delete=models.CASCADE, related_name="logs")

    action = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)

    data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.kyc_session.id}"