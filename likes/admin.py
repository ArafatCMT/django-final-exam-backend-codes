from django.contrib import admin
from likes.models import Like
# Register your models here.


class LikeAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'account']

    def post_id(self, obj):
        return f"post id: {obj.post.id}"
    

admin.site.register(Like,LikeAdmin)
