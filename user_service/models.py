from django.db import models
from core.models import User
from core.mixins import AbstractTrack
from django.utils.translation import gettext_lazy as _

class Customer(AbstractTrack):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)

    def __str__(self) -> str:
        return self.user.full_name

class Service(AbstractTrack):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="service")
    service_name = models.CharField(_("Service Name"), max_length=100)
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)

    def __str__(self) -> str:
        return self.user.full_name
