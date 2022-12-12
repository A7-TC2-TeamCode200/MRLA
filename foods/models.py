from django.db import models
from users.models import User


class Food(models.Model):
    class Meta:
        db_table = "food"

    food_id = models.IntegerField(primary_key=True, unique=True)
    menu = models.CharField(verbose_name="음식명", max_length=50)
    image = models.URLField(verbose_name="음식 사진", max_length=500)
    major_category = models.CharField(verbose_name="대분류", max_length=50)
    middle_category = models.CharField(verbose_name="중분류", max_length=50)
    minor_category = models.CharField(verbose_name="소분류", max_length=50)
    target = models.CharField(verbose_name="같이 먹는 대상", max_length=50)
    likes = models.ManyToManyField(User, verbose_name="좋아요 음식", through="FoodLike", related_name="food_likes", blank=True)

    def __str__(self):
        return str(self.menu)


class FoodLike(models.Model):
    class Meta:
        db_table = "food_like"

    user = models.ForeignKey(User, verbose_name="좋아요 등록 유저", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, verbose_name="음식명", on_delete=models.CASCADE)
    like = models.IntegerField(verbose_name="좋아요", default=True)

    def __str__(self):
        return str(f"{self.food} / {self.like}")


class FoodComment(models.Model):
    class Meta:
        db_table = "food_comment"

    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, related_name="foodcomment_user")
    menu = models.ForeignKey(Food, verbose_name="음식명", on_delete=models.CASCADE, related_name="foodcomment_menu", default="")
    comment = models.TextField(verbose_name="음식 댓글", max_length=500)
    created_at = models.DateTimeField(verbose_name="작성 시간", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정 시간", auto_now=True)

    def __str__(self):
        return str(f"{self.user} / {self.menu} / {self.comment}")


# # 어떤 방식으로 활용할지?
# class MajorCategories(models.Model):
#     major_category = models.CharField(max_length=20)

#     def __str__(self):
#         return self.major_category

# class MiddleCategories(models.Model):
#     middle_category = models.CharField(max_length=20)
#     major_category = models.ForeignKey("MajorCategories", on_delete=models.CASCADE, default="")

#     def __str__(self):
#         return self.middle_category

# class MinorCategories(models.Model):
#     minor_category = models.CharField(max_length=20)
#     middle_category = models.ForeignKey("MiddleCategories", on_delete=models.CASCADE, default="")
#     major_category = models.ForeignKey("MajorCategories", on_delete=models.CASCADE, default="")

#     def __str__(self):
#         return self.minor_category