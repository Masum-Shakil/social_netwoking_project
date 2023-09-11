from django import forms
from authentication_app.models import profile_models

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = profile_models.Profile
        fields = ('bio','profile_picture', 'facebook_link', 'linked_in_link', )
        exclude = ('user',)