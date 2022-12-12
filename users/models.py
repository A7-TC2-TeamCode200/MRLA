from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("이메일을 작성해 주세요.")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        error_messages={"unique": "이미 존재하는 이메일입니다."},
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    profile_img = models.ImageField(verbose_name="프로필 사진", default="profile/default.jpeg", upload_to="profile")
    nickname = models.CharField(verbose_name="닉네임", default="", max_length=20, unique=True, blank=True, error_messages={"unique": "이미 존재하는 닉네임입니다."})
    age = models.IntegerField(verbose_name="나이", null=True)
    gender = models.BooleanField(verbose_name="성별", null=True)
    major_category = models.CharField(verbose_name="선호하는 음식 종류", max_length=20, default="")

    following = models.ManyToManyField("self", verbose_name="팔로잉", symmetrical=False, blank=True, related_name="follower")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
