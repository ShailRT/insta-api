from rest_framework import serializers 
from .models import Post, Profile, Comment
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['caption', 'content', 'bg_music', 'category']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']