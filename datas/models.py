from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

from devices.models import Device
import csv


class Data(models.Model):
    """
    """
    device = models.ForeignKey(Device, related_name='device_data', on_delete=models.CASCADE)
    field_1 = models.CharField(_('Field 1'), max_length=10, null=True, blank=False)
    field_2 = models.CharField(_('Field 2'), max_length=10, null=True, blank=False)
    field_3 = models.CharField(_('Field 3'), max_length=10, null=True, blank=False)
    field_4 = models.CharField(_('Field 4'), max_length=10, null=True, blank=False)
    field_5 = models.CharField(_('Field 5'), max_length=10, null=True, blank=False)
    field_6 = models.CharField(_('Field 6'), max_length=10, null=True, blank=False)
    field_7 = models.CharField(_('Field 7'), max_length=10, null=True, blank=False)
    field_8 = models.CharField(_('Field 8'), max_length=10, null=True, blank=False)
    field_9 = models.CharField(_('Field 9'), max_length=10, null=True, blank=False)
    field_10 = models.CharField(_('Field 10'), max_length=10, null=True, blank=False)
    api_key = models.CharField(_('Api key'), max_length=200, null=True, blank=True)  # api key
    remote_address = models.CharField(_('Ip adres'), max_length=255)
    pub_date = models.DateTimeField(_('Publication date'), auto_now=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.device.name

    @staticmethod
    def get_as_csv(response):
        writer = csv.writer(response)
        data = Data.objects.all()
        writer.writerow(["Date", "Device", "Field_1", "Field_2", "Field_3", "Field_4", "Field_5", "Field_6",
                         "Field_7", "Field_8", "Field_9", "Field_10"])
        for entry in data:
            writer.writerow([entry.pub_date, entry.device, entry.field_1, entry.field_2, entry.field_3,
                             entry.field_4, entry.field_5, entry.field_6, entry.field_7, entry.field_8,
                             entry.field_9, entry.field_10])
        return response

