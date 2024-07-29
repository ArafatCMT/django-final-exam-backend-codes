from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
    # request.method jodi get, head, options hoi tobe shudu view korte dabo
    # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
         # opor er condition jodi true na hoi tobe put ba delete operation hobe
        return obj.account.user == request.user