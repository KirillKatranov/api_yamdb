from django.db import models
from django.utils import timezone
import datetime

class EmailVerificationCode(models.Model):
    email = models.EmailField()
    confirmation_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)