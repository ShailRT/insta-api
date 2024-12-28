from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from .models import Post, Profile, Comment
from .serializers import PostSerializer, ProfileSerializer, CommentSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    login(request,user)
    
    if user is not None:
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def user_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    login(request,user)

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        comments = Comment.objects.filter(post=post)
        comment_serializer = CommentSerializer(comments, many=True)
        response_data = serializer.data
        response_data['comments'] = comment_serializer.data
        return Response(response_data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
# @login_required(login_url='auth/login/')
@csrf_exempt
@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(user=request.user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
def follow_user(request, username):
    user = request.user 
    user_to_follow = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_to_follow)
    if user in profile.followers.all():
        profile.followers.remove(user)
        message = 'User unfollowed successfully'
    else:
        profile.followers.add(user)
        message = 'User followed successfully'
    profile.save()
    return Response({'message': message}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_user_posts(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# @login_required(login_url='auth/login/')
@api_view(['POST'])
def like_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
            message = 'Post unliked'
        else:
            post.liked_by.add(user)
            message = 'Post liked'
        post.save()
        return Response({'message': message}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post_likes(request, pk):
    post = Post.objects.get(id=pk)
    serializer = UserSerializer(post.liked_by, many=True)

    return Response(serializer.data)

# @login_required(login_url='auth/login/')
@api_view(['POST'])
def add_comment(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user, post=post)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def feed(request):
    user = request.user
    following = Profile.objects.filter(followers=user)
    users = User.objects.filter(profile__in=following)
    posts = Post.objects.filter(user__in=users).order_by('-date_posted') 
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
