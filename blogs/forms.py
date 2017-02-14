from django import forms


class BlogForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget = forms.Textarea)
    categories = forms.CharField()

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == "":
            raise forms.ValidationError("Title cannot be empty!")
        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == "":
            raise forms.ValidationError("Content cannot be empty!")
        return text

