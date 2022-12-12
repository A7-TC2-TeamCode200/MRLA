from django.db import models
from users.models import User
from django.urls import reverse


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_user")
    title = models.CharField(verbose_name="고객센터 게시글 제목", max_length=50)
    content = models.TextField(verbose_name="고객센터 게시글 내용")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} / {self.title}")


class ServiceComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="servicecomment_user")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="servicecomment_service")
    comment = models.TextField(verbose_name="고객센터 게시글 댓글 내용(운영진 전용)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.service} / {self.comment}")


class Community(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_user")
    title = models.CharField(verbose_name="커뮤니티 게시글 제목", max_length=50)
    content = models.TextField(verbose_name="커뮤니티 게시글 내용")
    image = models.ImageField(verbose_name="커뮤니티 사진", upload_to="community")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, verbose_name="좋아요 커뮤니티 게시글", related_name="community_likes", blank=True)

    def __str__(self):
        return str(f"{self.user} / {self.title}")

    def get_absolute_url(self):
        return reverse("community_comment_Detail_view", kwargs={"community_id": self.id})


class CommunityComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="communitycomment_user")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="comment_set")
    comment = models.TextField(verbose_name="커뮤니티 게시글 댓글 내용")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(f"{self.community} / {self.comment}")
