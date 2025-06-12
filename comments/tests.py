from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from users.models import User
from tweets.models import Tweet
from .models import Comment
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class CommentDeleteViewTest(APITestCase):
    # テストユーザーの作成
    @classmethod
    def setUpTestData(cls):
        # Original User
        cls.user = User.objects.create_user(
            username='origin',
            email='origin@gmail.com',
            telephone_number='080-1234-5678',
            password='password'
        )
        # Other User(権限確認用のダミーユーザー)
        cls.other_user = User.objects.create_user(
            username='other',
            email='other@gmail.com',
            telephone_number='080-1234-5678',
            password='password'
        )

        cls.tweet = Tweet.objects.create(
            user=cls.user,
            content='テスト用ツイート'
        )
    
    def setUp(self):
        # 標準のリクエストメソッド(put,delete,patch,etc...)が使えるようセットアップ
        self.client = APIClient()
        # Original Userでログイン
        self.client.force_authenticate(user = self.user)
    
    def test_delete_own_comment(self):
        """Comment作成者による削除可否のテスト"""
        comment = Comment.objects.create(user=self.user, tweet=self.tweet, comment='delete test')
        url = reverse('tweet_comments_delete', kwargs={'pk': comment.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_comment(self):
        """その他ユーザーが作成したCommentの削除不可のテスト"""
        comment = Comment.objects.create(user=self.other_user, tweet=self.tweet, comment='delete test')
        url = reverse('tweet_comments_delete', kwargs={'pk': comment.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
