from django.db import models
from posts.models import Post
from accounts.models import Account
# Create your models here.

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.description}"