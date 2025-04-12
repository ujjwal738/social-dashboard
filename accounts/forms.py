from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio', 'profile_picture',
            'twitter_handle', 'twitter_access_token', 'twitter_access_secret',
            'facebook_handle', 'facebook_access_token'
        ]
