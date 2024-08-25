from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User


# class OwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User

class CommentSerializer(serializers.ModelSerializer):
    
    owner_id = serializers.ReadOnlyField()
    post_id = serializers.ReadOnlyField()

    def create(self, validated_data):
        # Get the current request context
        request = self.context.get('request')
        post_id = self.context['post_id']
        owner = request.user if request else None  # Fallback to None if no request context is available
        return Comment.objects.create(post_id=post_id, owner=owner, **validated_data)
    
    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'content', 'owner_id', 'created_at', 'updated_at']

   

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    owner_id = serializers.ReadOnlyField()
    owner_username = serializers.SerializerMethodField(read_only=True)

    def get_owner_username(self, obj):
        return obj.owner.username
    

    def create(self, validated_data):
        # Get the current request context
        request = self.context.get('request')
        owner = request.user if request else None  # Fallback to None if no request context is available
        return Post.objects.create(owner=owner, **validated_data)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content','owner_username','owner_id', 'comments', 'created_at', 'updated_at']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content'
                 ]


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']