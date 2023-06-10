from django.db import models
from django.conf import settings

# Create your models here.

class User_info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    user_password = models.CharField(max_length=100)
    user_img = models.ImageField(upload_to='user-images/', null=True)

    def __str__(self):
        return self.user.username


CATEGORY_CHOICES = (
    ('Medical', 'Medical'),
    ('Science', 'Science'),
    ('Engineering', 'Engineering'),
    ('Environmental', 'Environmental'),
)

class Post(models.Model):
    author = models.ForeignKey(User_info, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    summary = models.TextField(max_length=200, null=True)
    content = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=14, null=True)
    created_at = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.user.username}"



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"All comments for {self.user.username}"