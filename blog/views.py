from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import CommentUpdateSerializer, PostSerializer, CommentSerializer, PostUpdateSerializer
from .permissions import IsOwnerOrReadOnly, IsOwnerOrPostOwner

class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.select_related('owner').all()
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    
    def get_serializer_class(self):
        # Use PostUpdateSerializer for update operations
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return PostUpdateSerializer
        return PostSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    
    @action(detail=False, methods=['GET'])
    def myposts(self, request):
        queryset = Post.objects.select_related('owner').filter(owner=request.user)
        count = queryset.count()
        serializer = PostSerializer(queryset, many=True)
        return Response({'posts': serializer.data
                        ,'count': count })
    

class CommentViewSet(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        # Use PostUpdateSerializer for update operations
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return CommentUpdateSerializer
        return CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPostOwner]

    def get_serializer_context(self):
        return {'request':self.request, 'post_id':self.kwargs['post_pk'] }
    

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user, post_id=self.kwargs['post_pk'])