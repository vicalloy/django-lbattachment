from django import forms
from lbutils import FormHelperMixin

from .models import LBAttachment


class LBAttachmentForm(FormHelperMixin, forms.ModelForm):

    class Meta:
        model = LBAttachment
        fields = ('attach_file',)
