from django import forms
from blog_app.models import post_models

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = post_models.Posts
        fields = ('post_title','post_details', 'picture',)
        exclude = ('created_by', 'created_at',)

class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = post_models.PostComments
        fields = ('comment_text',)
        exclude = ('created_by', 'created_at', 'blog_post',)