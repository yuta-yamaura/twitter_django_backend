from django.test import TestCase
from .models import User
from .models import Tweet
from django.core.exceptions import ValidationError

# Create your tests here.
class TweetCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test1',
            email='test1@gmail.com',
            telephone_number='080-1111-1111',
            password='password'
            )
    
    def setUp(self):
        # テストメソッド実行前にsetUpTestDataで作成したユーザーでログインする
        self.client.login(username='test1', password='password')
    
    def test_tweet_create_success(self):
        tweet = Tweet.objects.create(
            # self.userでクラス変数のcls.userにアクセス
            user = self.user,
            content = 'test',
        )
        new_tweet = Tweet.objects.get(user=tweet.user)
        self.assertEqual(new_tweet.user, self.user)
        self.assertEqual(new_tweet.content, 'test')

    def test_tweet_max_length_success(self):
        tweet = Tweet.objects.create(
            # self.userでクラス変数のcls.userにアクセス
            user = self.user,
            # ツイートの文言をmax_lengthの境界値である140文字に設定
            content = 'a' * 140,
        )
        tweet.full_clean()
        self.assertEqual(len(tweet.content), 140)

    def test_tweet_max_length_failed(self):
        tweet = Tweet(
            user = self.user,
            # ツイートの文章を141文字にしてバリデーションエラーを発生させるようにする
            content = 'a' * 141
        )
        with self.assertRaises(ValidationError):
            tweet.full_clean()
