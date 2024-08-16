from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=250, blank=True, null=True, default='https://i.ibb.co/XsJCM4t/image-placeholder-icon-11.png')

    phone_no = models.CharField(max_length=12, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class FriendRequest(models.Model):#
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')

class Friends(models.Model):#
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_account')
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE , related_name='sender_account')

    class Meta:
        verbose_name_plural = "Friends"