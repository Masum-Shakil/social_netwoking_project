from django.db import models
from django.contrib.auth.models import User

class Posts(models.Model):
    post_title = models.CharField(max_length=250)
    post_details = models.TextField()
    picture = models.ImageField(upload_to='post_picture')
    created_by = models.ForeignKey(User, related_name="post_user", on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title
    
class PostLikes(models.Model):
    liked_by = models.ForeignKey(User, related_name="post_like_user", on_delete=models.PROTECT)
    blog_post = models.ForeignKey(Posts, related_name="post_like", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('liked_by', 'blog_post',)

class PostComments(models.Model):
    created_by = models.ForeignKey(User, related_name="comment_user", on_delete=models.PROTECT)
    blog_post = models.ForeignKey(Posts, related_name="comment_post", on_delete=models.PROTECT)
    comment_text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

class PostSharings(models.Model):
    shared_by = models.ForeignKey(User, related_name="post_share_user", on_delete=models.PROTECT)
    blog_post = models.ForeignKey(Posts, related_name="post_share", on_delete=models.PROTECT)

    class Meta:
        unique_together = ('shared_by', 'blog_post',)
