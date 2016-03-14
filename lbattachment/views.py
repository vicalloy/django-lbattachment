import os
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect

from lbutils.views import render_json
from .forms import LBAttachmentForm
from .models import LBAttachment
from . import settings as lb_settings


@csrf_exempt
def upload__(request):
    ret = {}
    if not request.user.is_authenticated():
        return render_json(ret)
    form = LBAttachmentForm()
    if request.method == "POST":
        form = LBAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            ret['valid'] = True
            ret['file'] = {
                'id': obj.id,
                'fn': obj.org_filename,
                'url': obj.file.url,
                'descn': ''}
        else:
            ret['valid'] = True
            ret['errors'] = form.errors_as_text()
    return render_json(ret)


@login_required
def download(request):
    pk = request.GET.get('pk')
    response = HttpResponse('')
    obj = get_object_or_404(LBAttachment, pk=pk)
    fn = os.path.join(lb_settings.LBATTACHMENT_MEDIA_URL, obj.file.name)
    if not lb_settings.LBATTACHMENT_X_ACCEL:
        return redirect(fn)
    response['X-Accel-Redirect'] = fn.encode('UTF-8')
    response["Content-Disposition"] = "attachment; filename={0}".\
        format(obj.filename).encode('utf-8')
    response['Content-Type'] = ''
    return response


@csrf_exempt
def delete__(request):
    ret = {}
    attachment_id = request.POST.get('id', 0) or request.GET.get('id', 0)
    attachment = LBAttachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        ret['valid'] = False
        ret['errors'] = _('no right')
    else:
        attachment.delete()
        ret['valid'] = True
    return render_json(ret)


@csrf_exempt
def change_descn__(request):
    ret = {'valid': False, 'errors': ''}
    pk = request.POST.get('pk', 0) or request.GET.get('pk', 0)
    attachment = get_object_or_404(LBAttachment, pk=pk)
    if not attachment:
        ret['valid'] = False
        ret['errors'] = _("This file could't be find.")
        return render_json(ret)
    if (attachment.user != request.user):
        ret['valid'] = False
        ret['errors'] = _('no right')
        return render_json(ret)
    if request.method == "POST":
        attachment.description = request.POST.get('descn', '')
        ret['valid'] = True
        attachment.save()
    return render_json(ret)
