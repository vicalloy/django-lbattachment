from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from . import settings as lb_settings
from .forms import LBAttachmentForm
from .models import LBAttachment


@csrf_exempt
def upload__(request):
    ctx = {}
    if callable(request.user.is_authenticated):
        is_authenticated = request.user.is_authenticated()
    else:
        is_authenticated = request.user.is_authenticated
    if not is_authenticated:
        ctx['valid'] = False
        ctx['errors'] = _('Please login first.')
        return JsonResponse(ctx)
    form = LBAttachmentForm()
    if request.method == "POST":
        form = LBAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            ctx['valid'] = True
            ctx['file'] = {
                'pk': obj.pk,
                'fn': obj.filename,
                'url': "%s?pk=%s" % (reverse('lbattachment_download'), obj.pk),
                'descn': obj.description}
        else:
            ctx['valid'] = False
            ctx['errors'] = form.errors_as_text()
    return JsonResponse(ctx)


@login_required
def download(request):
    pk = request.GET.get('pk')
    response = HttpResponse('')
    obj = get_object_or_404(LBAttachment, pk=pk)
    fn = obj.attach_file.name
    if not lb_settings.LBATTACHMENT_X_ACCEL:
        return redirect(obj.attach_file.url)
    response['X-Accel-Redirect'] = fn.encode('UTF-8')
    response["Content-Disposition"] = "attachment; filename={0}".\
        format(obj.filename).encode('utf-8')
    response['Content-Type'] = ''
    return response


@csrf_exempt
def delete__(request):
    ctx = {}
    attachment_pk = request.POST.get('pk', 0) or request.GET.get('pk', 0)
    attachment = LBAttachment.objects.get(pk=attachment_pk)
    if (attachment.created_by != request.user):
        ctx['valid'] = False
        ctx['errors'] = _('no right')
    else:
        attachment.delete()
        ctx['valid'] = True
    return JsonResponse(ctx)


@csrf_exempt
def change_descn__(request):
    ctx = {'valid': False, 'errors': ''}
    pk = request.POST.get('pk', 0) or request.GET.get('pk', 0)
    attachment = get_object_or_404(LBAttachment, pk=pk)
    if not attachment:
        ctx['valid'] = False
        ctx['errors'] = _("This file could't be find.")
        return JsonResponse(ctx)
    if attachment.created_by != request.user:
        ctx['valid'] = False
        ctx['errors'] = _('no right')
        return JsonResponse(ctx)
    if request.method == "POST":
        attachment.description = request.POST.get('descn', '')
        ctx['valid'] = True
        attachment.save()
    return JsonResponse(ctx)
