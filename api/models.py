from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    content = models.FileField(upload_to='content/')
    bg_music = models.FileField(upload_to='bg_music/', blank=True, null=True)
    category = models.CharField(max_length=100)
    liked_by = models.ManyToManyField(User, related_name='liked_by', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.caption
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    bio = models.TextField()
    followers = models.ManyToManyField(User, related_name='followers', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content