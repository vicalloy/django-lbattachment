import django.dispatch
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from lbutils.views import render_json
from .forms import LBAttachmentForm
from .models import LBAttachment


@csrf_exempt
@login_required
def ajax_upload(request):
    ret = {'valid': False, 'errors': ugettext('no file')}
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
            ret.pop('errors')
            ret['file'] = {
                'id': obj.id,
                'fn': obj.org_filename,
                'url': obj.file.url,
                'descn': ''}
        else:
            pass
    return render_json(ret)


@csrf_exempt
@login_required
def ajax_delete(request):
    data = {'valid': False, 'errors': ugettext('some errors...')}
    attachment_id = request.POST.get('id', 0) or request.GET.get('id', 0)
    attachment = LBAttachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        data['errors'] = ugettext('no right')
    else:
        attachment.delete()
        data['valid'] = True
        data.pop('errors')
    return render_json(data)


@csrf_exempt
@login_required
def ajax_change_descn(request):
    data = {'valid': False, 'errors': ugettext('some errors...')}
    attachment_id = request.POST.get('id', 0) or request.GET.get('id', 0)
    attachment = LBAttachment.objects.get(pk=attachment_id)
    if (attachment.user != request.user):
        data['errors'] = ugettext('no right')
    elif request.method == "POST":
        attachment.description = request.POST['descn']
        data['valid'] = True
        data.pop('errors')
        attachment.save()
    return render_json(data)

upload_recieved = django.dispatch.Signal(providing_args=['data'])
