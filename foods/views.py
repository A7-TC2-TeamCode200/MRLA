from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from foods.models import Food, FoodComment
from foods.serializers import FoodSerializer, FilteringFoodSerializer, FoodCommentSerializer, FoodCommentCreateSerializer
from foods.collaborative_filtering import collaborative_filtering


# 전체 메뉴 리스트 조회
class FoodView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 메뉴 상세 페이지
class FoodDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, food_id):
        food = get_object_or_404(Food, food_id=food_id)
        serializer = FoodSerializer(food)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 메뉴에 대한 댓글 CRUD
class FoodCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, food_id):
        food = get_object_or_404(Food, food_id=food_id)
        comments = food.foodcomment_menu.all()
        serializer = FoodCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, food_id):
        serializer = FoodCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, menu_id=food_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, food_id, comment_id):
        comment = get_object_or_404(FoodComment, id=comment_id)
        if request.user == comment.user:
            serializer = FoodCommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, food_id, comment_id):
        comment = get_object_or_404(FoodComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_401_UNAUTHORIZED)
       

# 추천 음식 리스트 조회
class FilteringFoodView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        food_list = []
        foods = collaborative_filtering(request.user.id)
        for food in foods:
            recommend_food = get_object_or_404(Food, food_id=food)
            if recommend_food.major_category == request.user.major_category:
                if len(food_list) < 7:
                    food_list.append(recommend_food)
                else:
                    serializer = FilteringFoodSerializer(food_list, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)


# 메뉴 좋아요 등록/취소
class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, food_id):
        food = get_object_or_404(Food, food_id=food_id)
        if request.user in food.likes.all():
            food.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            food.likes.add(request.user)
            return Response("좋아요!", status=status.HTTP_200_OK)


# 프로필 페이지 _ 프로필 유저가 좋아요 등록한 메뉴 리스트 조회
class LikeFoodListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        foods = user.food_likes.all()
        serializer = FilteringFoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        




