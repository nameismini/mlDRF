from django.db import models
from django.utils import timezone

# Create your models here.


class LogInfo(models.Model):
    restGbn = models.CharField(max_length=128)
    crudMod = models.CharField(max_length=128, default='')
    remark = models.CharField(max_length=128)
    temp1 = models.CharField(max_length=128)
    temp2 = models.CharField(max_length=128)
    reg_date = models.DateTimeField(default=timezone.now())