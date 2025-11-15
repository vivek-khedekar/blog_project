from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BlogPost, Comment, Like
from .serializers import BlogPostSerializer, CommentSerializer
from .permissions import IsAuthorOrAdminOrReadOnly



class BlogViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    

    lookup_field = 'id'   # Use custom ID field instead of pk

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # -----------------------------------------------------------
    # LIKE / UNLIKE BLOG
    # -----------------------------------------------------------
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, id=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=200)

        return Response({'status': 'liked'}, status=200)

    # -----------------------------------------------------------
    # CREATE COMMENT
    # -----------------------------------------------------------
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, id=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # -----------------------------------------------------------
    # GET ALL COMMENTS FOR A BLOG
    # -----------------------------------------------------------
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def comments(self, request, id=None):
        post = self.get_object()
        comments = post.comments.all().order_by('-created_at')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


# -------------------------------------------------------------------
# COMMENT CRUD for editing/deleting comments
# -------------------------------------------------------------------

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]


