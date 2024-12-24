from django.contrib.auth.models import AbstractUser
from django.db import models
from core.mixins import AbstractTrack
from django.utils.translation import gettext_lazy as _

class User(AbstractUser, AbstractTrack):
    email = models.EmailField(_("Email Address"), unique=True)
    mobile = models.CharField(_("Mobile Number"), max_length=15, unique=True)
    is_email_verified = models.BooleanField(_("Email Verified"), default=False)
    full_name = models.CharField(_("Full Name"), max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
