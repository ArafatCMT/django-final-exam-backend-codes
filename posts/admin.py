from django.contrib import admin
from posts.models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['post_onwer' , 'image_url']

    def post_onwer(self, obj):
        return f"{obj.account.user.first_name} {obj.account.user.last_name}"
    
admin.site.register(Post, PostAdmin)
