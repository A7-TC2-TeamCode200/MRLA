from rest_framework import serializers
from posts.models import Service, ServiceComment, Community, CommunityComment


# 고객센터 게시글 조회
class ServiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Service
        fields = ("id", "user", "title", "created_at")


# 고객센터 게시글 등록
class ServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("title", "content")


# 고객센터 게시글 디테일 조회
class ServiceDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Service
        fields = ("user", "title", "content", "created_at")


# 고객센터 게시글 디테일 댓글 조회
class ServiceCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = ServiceComment
        fields = ("user", "service", "comment", "created_at", "updated_at")


# 고객센터 게시글 디테일 댓글 등록
class ServiceCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceComment
        fields = ("comment",)


# 커뮤니티 게시글 댓글 조회
class CommunityCommentSerializer(serializers.ModelSerializer):
    community_id = serializers.SerializerMethodField()
    community_content = serializers.SerializerMethodField()

    def get_community_id(self, obj):
        return obj.community.id

    def get_community_content(self, obj):
        return obj.community.content

    class Meta:
        model = CommunityComment
        fields = ("id", "community_id", "community_content", "comment", "created_at", "updated_at")


# 커뮤니티 게시글 조회
class CommunitySerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Community
        fields = '__all__'

# # 커뮤니티 게시글 조회
# class CommunityListSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
#     comment_set = serializers.SerializerMethodField()

#     def get_user(self, obj):
#         return obj.user.email

#     def get_comment_set(self, obj):
#         return obj.comment_set.count()

#     class Meta:
#         model = Community
#         fields = ("pk", "title", "image", "updated_at", "user", "comment_set")


# 커뮤니티 게시글 등록
class CommunityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("title", "content", "image")


# 커뮤니티 게시글 댓글 등록
class CommunityCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = ("comment", )
