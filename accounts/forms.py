from django.forms import ModelForm
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'mobile', 'residence', 'website', 'microblog', 'qq', 'wechat', 'introduction']
