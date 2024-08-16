from django.contrib import admin
from accounts.models import Account, FriendRequest, Friends
# Register your models here.

admin.site.register(Account)

class FrinedRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver']

    def sender(self, obj):
        return f"{obj.sender.user.first_name} {obj.sender.user.last_name}"
    
    def receiver(self, obj):
        return f"{obj.receiver.user.first_name} {obj.receiver.user.last_name}"
    
admin.site.register(FriendRequest, FrinedRequestAdmin)

class FriendAdmin(admin.ModelAdmin):
    list_display=['sender', 'receiver']

    def sender(self, obj):
        return f"{obj.sender_account.user.first_name} {obj.sender_account.user.last_name}"
    
    def receiver(self, obj):
        return f"{obj.receiver_account.user.first_name} {obj.receiver_account.user.last_name}"
    
admin.site.register(Friends,FriendAdmin)