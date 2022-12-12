from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users.models import User
from posts.models import Service, Community, CommunityComment
from posts.serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    ServiceDetailSerializer,
    ServiceCommentSerializer,
    ServiceCommentCreateSerializer,
    CommunitySerializer,
    CommunityCreateSerializer,
    CommunityCommentSerializer,
    CommunityCommentCreateSerializer,
)


# 고객센터 게시글 조회/등록
class ServiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Service.objects.all().order_by("-id")
        serializer = ServiceSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = ServiceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 고객센터 게시글 디테일 조회
class ServiceDetailtView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        if request.user == service.user or request.user.is_admin:
            serializer = ServiceDetailSerializer(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_401_UNAUTHORIZED)


# 고객센터 게시글 디테일 댓글 조회/등록
class ServiceCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        comments = service.servicecomment_service.all()
        if request.user == service.user or request.user.is_admin:
            serializer = ServiceCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, service_id):
        serializer = ServiceCommentCreateSerializer(data=request.data)
        if request.user.is_admin:
            if serializer.is_valid():
                serializer.save(user=request.user, service_id=service_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다!"}, status=status.HTTP_401_UNAUTHORIZED)


# 커뮤니티 게시글 조회/등록
class CommunityView(APIView):
    def get(self, request):
        communities = Community.objects.all().order_by("-id")
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = CommunityCreateSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 커뮤니티 게시글 수정/삭제
class CommunityDetailView(APIView):
    def get(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        serializer = CommunitySerializer(community)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, community_id):

        community = get_object_or_404(Community, id=community_id)

        if request.user == community.user:
            serializer = CommunityCreateSerializer(community, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, community_id):

        community = get_object_or_404(Community, id=community_id)

        if request.user == community.user:
            community.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)


# 커뮤니티 게시글 댓글 조회/등록
class CommunityCommentView(APIView):
    def get(self, request, community_id):
        community = Community.objects.get(id=community_id)
        comments = community.comment_set.all().order_by("-id")
        serializer = CommunityCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, community_id):
        serializer = CommunityCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, community_id=community_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 커뮤니티 게시글 댓글 수정/삭제
class CommunityCommentDetailView(APIView):
    def put(self, request, community_id, comment_id):
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user == comment.user:
            serializer = CommunityCommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, community_id, comment_id):
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status = status.HTTP_403_FORBIDDEN)
        

# 커뮤니티 게시글 좋아요 등록/취소
class CommunityLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        if request.user in community.likes.all():
            community.likes.remove(request.user)
            return Response("좋아요 취소", status=status.HTTP_200_OK)
        else:
            community.likes.add(request.user)
            return Response("좋아요!", status=status.HTTP_200_OK)


# 프로필 페이지 _ 프로필 유저가 좋아요 등록한 커뮤니티 게시글 목록 조회
class LikeCommunityListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        community = user.community_likes.all()
        serializer = CommunitySerializer(community, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

