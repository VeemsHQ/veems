from django import forms

from ..channel import models


class ChannelForm(forms.ModelForm):

    class Meta:
        model = models.Channel
        fields = ['name', 'description']
