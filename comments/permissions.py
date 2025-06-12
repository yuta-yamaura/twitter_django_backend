from rest_framework import permissions, exceptions

class CommentCreateOrDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # コメントの所有者の場合
        if obj.user != request.user:
            raise exceptions.AuthenticationFailed('このコメントを削除する権限がありません')
        return True
