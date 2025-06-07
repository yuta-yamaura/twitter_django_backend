from rest_framework import permissions

class CommentCreateOrDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('requestの中身', request)
        print('permission objの中身', obj)
        # コメントの所有者の場合
        if obj.user == request.user:
            if request.method in permissions.SAFE_METHODS:
                return True
            # 登録、削除を許可
            return request.method in ["PUT", "DELETE"]

        # その他のユーザーは読み取りのみ許可
        return request.method in permissions.SAFE_METHODS
