from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class LogInfo(models.Model):
    restGbn = models.CharField(max_length=128)
    crudMod = models.CharField(max_length=128, default='')
    remark = models.CharField(max_length=128)
    temp1 = models.CharField(max_length=128)
    temp2 = models.CharField(max_length=128)
    reg_date = models.DateTimeField(default=timezone.now)

#LogInfo 모델이 post 액션을 일이키고 save 모드가 된다면 실행한다
@receiver(post_save, sender=LogInfo)
def create_user_profile(sender, instance, created, **kwargs):
    # if created:
        # Profile.objects.create(user=instance)
    return print('receiver')