from rest_framework import permissions, exceptions

class CreateUserEditOrDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # ツイートの所有者の場合
        if obj.user == request.user:
            if request.method in permissions.SAFE_METHODS:
                return True
            # 登録、編集、削除を許可
            return request.method in ["PUT", "PATCH", "DELETE"]

        # その他のユーザーは読み取りのみ許可
        return request.method in permissions.SAFE_METHODS   

class TweetDeletePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed('認証が必要です')
        return True

    def has_object_permission(self, request, view, obj):
        if obj.user != request.user:
            raise exceptions.AuthenticationFailed('このツイートを削除する権限がありません')
        return True
