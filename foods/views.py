from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from foods.models import Food
from foods.serializers import FoodSerializer, FilteringFoodSerializer
from foods.collaborative_filtering import collaborative_filtering


# 메뉴 리스트 조회 (좋아요 등록 많은 순서대로)
class FoodList(APIView):
    def get(self, request):
        foods = Food.objects.all().order_by("-likes")
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 추천 음식 리스트 조회
class FilteringFoodView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, food_id):
        food_list = []
        foods = collaborative_filtering(request.user.id)
        like_food = get_object_or_404(Food, food_id=food_id)
        for food in foods:
            recommend_food = get_object_or_404(Food, food_id=food)
            if recommend_food.major_category == like_food.major_category:
                if len(food_list) < 5:
                    food_list.append(recommend_food)
                else:
                    serializer = FilteringFoodSerializer(food_list, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)


# 메뉴 좋아요 리스트(보류)
# class FoodLikeView(APIView):
#     def get(self, request):
#         food_like = FoodLike.objects.filter(id__isnull=False).order_by("user_id")
#         food_like_list = serializers.serialize('json', food_like)
#         return HttpResponse(food_like_list, content_type="text/json-comment-filtered")


# 메뉴 좋아요 등록/취소
class LikeView(APIView):
    def post(self, request, food_id):
        food = get_object_or_404(Food, food_id=food_id)
        if request.user in food.likes.all():
            food.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            food.likes.add(request.user)
            return Response("좋아요!", status=status.HTTP_200_OK)