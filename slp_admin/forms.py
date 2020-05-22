from django import forms
from . import models


class AddVideoForm(forms.ModelForm):
    class Meta:
        model = models.Video
        fields = ('category', 'title', 'description', 'video')
