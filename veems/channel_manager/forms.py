from django import forms

from ..channel import models


class ChannelForm(forms.ModelForm):
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = models.Channel
        fields = ['name', 'description']

