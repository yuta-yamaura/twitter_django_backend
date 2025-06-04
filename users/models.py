from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, telephone_number, password=None):
        if not email:
            raise ValueError('メールアドレスは必須です')
        if not username:
            raise ValueError('ユーザー名は必須です')
        if not password:
            raise ValueError('パスワードは必須です')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            telephone_number=telephone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, telephone_number, password=None):
        user = self.create_user(
            username,
            email,
            telephone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(null=False, unique=True, max_length=22)
    email = models.EmailField(null=False)
    telephone_number = models.CharField(null=False, max_length=13)
    account_name = models.CharField(null=True, max_length=12)
    self_introduction = models.TextField(null=True)
    address = models.TextField(null=True)
    web_site = models.TextField(null=True)
    date_of_birth = models.DateField(null=True)
    image = models.ImageField(null=True)
    background_image = models.ImageField(null=True)
    avater = models.ImageField(null=True)
    follow = models.IntegerField(null=True)
    info_flg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'telephone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin