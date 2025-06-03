from django.test import TestCase
from .models import User
from django.core.exceptions import ValidationError

# Create your tests here.
class UserTestCase(TestCase):
    # ユーザ名がNullのパターン
    def test_username_nullerror(self):
        user = User(
            username='',
            email='test@gmail.com',
            telephone_number='080-1234-5678',
            password='password',
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    # ユーザ名が長すぎるバリデーションエラーのパターン
    def test_username_validationerror(self):
        user = User(
            username='a' * 23,
            email='test@gmail.com',
            telephone_number='080-1234-5678',
            password='password',
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    # EmailがNullのパターン
    def test_email_nullerror(self):
        user = User(
            username='test',
            email='',
            telephone_number='080-1234-5678',
            password='password',
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    # telephone_numberがNullのパターン
    def test_telephone_number_nullerror(self):
        user = User(
            username='test',
            email='test@gmail.com',
            telephone_number='',
            password='password',
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    # telephone_numberが長すぎるバリデーションエラーのパターン
    def test_telephone_number_validationerror(self):
        user = User(
            username='test',
            email='test@gmail.com',
            telephone_number='080-1234-56789',
            password='password',
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

class SignUp_Login_ViewSuccessTest(TestCase):
    def setUp(self):
        self.url = '/api/users/login/'
        user = User.objects.create_user(
                username='test1',
                email='test1@gmail.com',
                telephone_number='080-1111-1111',
                password='password'
            )
        user.save()

    def test_signup_view_success(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)

    def test_login_success(self):
        data = {
            "username": 'test1',
            "password": 'password'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

class SignUp_Login_ViewFailedTest(TestCase):
    def test_signup_view_mail_null_faild(self):
        with self.assertRaises(ValueError, msg='メールアドレスは必須です'):
                user = User.objects.create_user(
                    username='test1',
                    email=None,
                    telephone_number='080-1111-1111',
                    password='password'
                )
                user.save()
    
    def test_signup_view_username_null_faild(self):
        with self.assertRaises(ValueError, msg='ユーザー名は必須です'):
                user = User.objects.create_user(
                    username=None,
                    email='test@gmail.com',
                    telephone_number='080-1111-1111',
                    password='password'
                )
                user.save()
    
    def test_signup_view_password_null_faild(self):
        with self.assertRaises(ValueError, msg='パスワードは必須です'):
                user = User.objects.create_user(
                    username='test',
                    email='test@gmail.com',
                    telephone_number='080-1111-1111',
                    password=None
                )
                user.save()
