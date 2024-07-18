from django.db import models
from accounts.models import Account
from posts.models import Post
# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"comment by : {self.account.user.first_name}"
