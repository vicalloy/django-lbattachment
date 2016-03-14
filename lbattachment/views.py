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
    ctx = {}
    if not request.user.is_authenticated():
        return render_json(ctx)
    form = LBAttachmentForm()
    if request.method == "POST":
        form = LBAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            ctx['valid'] = True
            ctx['file'] = {
                'id': obj.id,
                'fn': obj.org_filename,
                'url': obj.file.url,
                'descn': ''}
        else:
            ctx['valid'] = True
            ctx['errors'] = form.errors_as_text()
    return render_json(ctx)


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
    ctx = {}
    attachment_id = request.POST.get('id', 0) or request.GET.get('id', 0)
    attachment = LBAttachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        ctx['valid'] = False
        ctx['errors'] = _('no right')
    else:
        attachment.delete()
        ctx['valid'] = True
    return render_json(ctx)


@csrf_exempt
def change_descn__(request):
    ctx = {'valid': False, 'errors': ''}
    pk = request.POST.get('pk', 0) or request.GET.get('pk', 0)
    attachment = get_object_or_404(LBAttachment, pk=pk)
    if not attachment:
        ctx['valid'] = False
        ctx['errors'] = _("This file could't be find.")
        return render_json(ctx)
    if (attachment.user != request.user):
        ctx['valid'] = False
        ctx['errors'] = _('no right')
        return render_json(ctx)
    if request.method == "POST":
        attachment.description = request.POST.get('descn', '')
        ctx['valid'] = True
        attachment.save()
    return render_json(ctx)
