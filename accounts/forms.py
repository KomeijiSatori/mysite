from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'birthday', 'mobile', 'residence', 'website', 'microblog', 'qq', 'wechat', 'introduction']
        labels = {
            'gender': _('gender'),
            'birthday': _('birthday'),
            'mobile': _('mobile'),
            'residence': _('residence'),
            'website': _('website'),
            'microblog': _('microblog'),
            'qq': _('QQ'),
            'wechat': _('wechat'),
            'introduction': _('introduction'),
        }
