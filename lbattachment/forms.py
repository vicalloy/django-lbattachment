from django import forms

from models import LBAttachment


class LBAttachmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.actived = kwargs.pop('actived', False)
        super(LBAttachmentForm, self).__init__(*args, **kwargs)

    def save(self):
        attachment = super(LBAttachmentForm, self).save(commit=False)
        attachment.user = self.user
        attachment.actived = self.actived
        attachment.save()
        return attachment

    class Meta:
        model = LBAttachment
        fields = ('file',)
