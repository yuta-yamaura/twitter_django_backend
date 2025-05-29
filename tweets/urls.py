from rest_framework.routers import DefaultRouter
from .views import TweetViewSet

# DefaultRouterを使いCRUDエンドポイントを自動生成
router = DefaultRouter()
router.register(r'tweets', TweetViewSet, basename='tweets')

urlpatterns = router.urls
