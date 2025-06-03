from .models import User
from .models import Tweet
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
class TweetCreateViewTest(APITestCase):
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
    
    def setUp(self):
        # 標準のリクエストメソッド(put,delete,patch,etc...)が使えるようセットアップ
        self.client = APIClient()
        # リクエストを強制的に認証
        self.client.force_authenticate(user=self.user)
    
    def test_tweet_create_success(self):
        """Tweet作成のテスト"""
        url = reverse('tweets-list')
        data = {'content': 'create test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 1)
        self.assertEqual(Tweet.objects.get().content, 'create test')
        self.assertEqual(Tweet.objects.get().user, self.user)

    def test_tweet_max_length_success(self):
        """最大文字数(140文字)のTweetの作成"""
        url = reverse('tweets-list')
        data = {'content': 'a' * 140}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Tweet.objects.get().content), 140)
    
    def test_tweet_maximum_number_of_characters_exceeded(self):
        """最大文字数超過(141文字)のTweetの作成"""
        url = reverse('tweets-list')
        data = {'content': 'a' * 141}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
