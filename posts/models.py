from django.db import models
from accounts.models import Account
# Create your models here.

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete= models.CASCADE)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"post id: {self.id}"
