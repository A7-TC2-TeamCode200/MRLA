import re
from users.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 회원 가입/수정(정규식 적용)
class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(error_messages={"write_only": True, "required": "비밀번호 확인까지 입력해 주세요.", "blank": "비밀번호 확인까지 입력해 주세요."})

    class Meta:
        model = User
        fields = ("email", "nickname", "password", "password_check", "major_category")
        extra_kwargs = {
            "email": {"error_messages": {"required": "이메일을 입력해 주세요.", "blank": "이메일을 입력해 주세요."}},
            "nickname": {"error_messages": {"required": "닉네임을 입력해 주세요.", "blank": "닉네임을 입력해 주세요."}},
            "password": {"write_only": True, "error_messages": {"required": "비밀번호를 입력해 주세요.", "blank": "비밀번호를 입력해 주세요."}},
            "major_category": {"error_messages": {"required": "카테고리를 입력해 주세요.", "blank": "카테고리를 입력해 주세요."}},
        }

    def validate(self, validated_data):
        email = validated_data.get("email")
        email_reg = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        password = validated_data.get("password")
        password_reg = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$"
        password_check = validated_data.get("password_check")

        # 이메일 유효성 체크
        if not re.search(email_reg, str(email)):
            raise serializers.ValidationError(detail={"email": "이메일 형식에 맞춰서 작성해 주세요."})

        # 비밀번호 유효성 체크
        if not re.search(password_reg, str(password)):
            raise serializers.ValidationError(detail={"password": "최소 한 개의 영문자와 숫자를 포함해 5글자 이상으로 만들어 주세요."})
        elif password != password_check:
            raise serializers.ValidationError(detail={"password": "동일한 비밀번호를 입력해 주세요."})

        return validated_data

    def create(self, validated_data):
        email = validated_data["email"]
        nickname = validated_data["nickname"]
        password = validated_data["password"]
        major_category = validated_data["major_category"]
        user = User(email=email, nickname=nickname, password=password, major_category=major_category)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def update(self, validated_data):
        email = validated_data["email"]
        nickname = validated_data["nickname"]
        password = validated_data["password"]
        major_category = validated_data["major_category"]
        user = User(email=email, nickname=nickname, password=password, major_category=major_category)
        user.set_password(password)
        user.save()
        return user


# 토큰 정보 커스텀
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token


# 프로필 조회
class ProfileSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "profile_img", "nickname", "age", "gender", "follower")


# 프로필 수정
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_img", "nickname", "age", "gender")


# 팔로잉/팔로워 리스트 조회
class FollowSerializer(serializers.ModelSerializer):
    following = serializers.StringRelatedField(many=True)
    follower = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = User
        fields = ("following", "follower")
