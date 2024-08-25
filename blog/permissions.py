from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user
    

class IsOwnerOrPostOwner(permissions.BasePermission):
    """
    Custom permission to allow only the comment owner or post owner to modify comments.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the comment owner
        if request.method in permissions.SAFE_METHODS: 
            return True

        if request.user == obj.owner:
            return True

        # Check if the user is the post owner
        if request.user == obj.post.owner:
            return request.method == 'DELETE'  # Only allow deletion for post owner

        return False