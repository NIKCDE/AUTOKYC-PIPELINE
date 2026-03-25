from django.db import models
from kyc.models import KYCSession

class Document(models.Model):
    DOC_TYPES = [
        ('ID', 'ID Document'),
        ('SELFIE', 'Selfie'),
    ]

    kyc_session = models.ForeignKey(KYCSession, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=10, choices=DOC_TYPES)
    file = models.ImageField(upload_to='kyc/')

    uploaded_at = models.DateTimeField(auto_now_add=True)