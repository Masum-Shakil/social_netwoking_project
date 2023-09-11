from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture', null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    linked_in_link = models.URLField(null=True, blank=True)
    # Add any other fields you want for the user's profile

    def __str__(self):
        return self.user.username
    
class FriendshipModels(models.Model):
    from_friend_request = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="from_profile")
    to_friend_request = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="to_profile")
    friend_request_status = models.CharField(max_length=10)

    def clean(self):
        
        if self.from_friend_request == self.to_friend_request:
            raise ValidationError('From friend request and to friend request should be different.')
        
    class Meta:
        unique_together = ('from_friend_request', 'to_friend_request')    