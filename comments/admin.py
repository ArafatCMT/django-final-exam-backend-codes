from django.contrib import admin
from comments.models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'comment_by']

    def comment_by(self,obj):
        return f"{obj.account.user.first_name} {obj.account.user.last_name}"


admin.site.register(Comment,CommentAdmin)
