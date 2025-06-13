from rest_framework import permissions

class UserProfileEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # ログインユーザー自身のプロフィールの場合
        if obj.id == request.user.id:  # ユーザーIDで比較
            if request.method in permissions.SAFE_METHODS:
                return True
            # 登録、編集を許可
            return request.method in ["PUT", "PATCH"]

        # その他のユーザーは読み取りのみ許可
        return request.method in permissions.SAFE_METHODS
