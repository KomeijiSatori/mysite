import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from pagedown.widgets import PagedownWidget


class BlogForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': _('Title')}))
    categories = forms.CharField(required=False, label='', widget=forms.TextInput(
        attrs={'placeholder': _('Tags    Divide tags by space, could be empty')}))
    text = forms.CharField(label='', widget=PagedownWidget(show_preview=False))

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == "":
            raise forms.ValidationError(_("Title cannot be empty!"))
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == "":
            raise forms.ValidationError(_("Content cannot be empty!"))
        http_links = re.findall(r'\[\d+\]: http://[^\s]*', text)
        if len(http_links) > 0:
            raise forms.ValidationError(str(_("Http link found! Only Https link is allowed! ")) + " ".join(http_links))
        return text

    def clean_categories(self):
        category_text = self.cleaned_data.get('categories')
        category = category_text.split(' ')
        if category_text == '':
            return category_text
        if '' in category:
            raise forms.ValidationError(_("Too many spaces between tags!"))
        if len(category) != len(set(category)):
            raise forms.ValidationError(_("Redundant tags exist!"))
        return category_text


class BlogCommentForm(forms.Form):
    text = forms.CharField(label="", help_text="", widget=forms.Textarea)

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == "":
            raise forms.ValidationError(_("Content cannot be empty!"))
        return text
