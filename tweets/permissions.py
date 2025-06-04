from rest_framework import permissions

class CreateUserEditOrDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # super userは全ての操作が可能
        if request.user.is_superuser:
            return True

        # ツイートの所有者の場合
        if obj.user == request.user:
            if request.method in permissions.SAFE_METHODS:
                return True
            # 登録、編集、削除を許可
            return request.method in ["PUT", "PATCH", "DELETE"]

        # その他のユーザーは読み取りのみ許可
        return request.method in permissions.SAFE_METHODS
