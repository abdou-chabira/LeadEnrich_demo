import uuid
from django.db import models

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    enriched = models.BooleanField(default=False)
    enrichment_data = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending","Pending"),("processing","Processing"),("completed","Completed"),("failed","Failed")],
        default="pending"
    )
    retry_count = models.IntegerField(default=0)
    idempotency_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)