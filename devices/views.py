import uuid

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from devices.forms import DeviceForm
from devices.models import Device
from iotdashboard.settings import LOGIN_URL
from datas.models import Data
from util.HiveMQ import PublicClient


def index(request):
    """
    :param request:
    :return:
    """
    panel = True
    # auto login for test users
    # admin:Aa1234567890
    user = authenticate(username='admin', password='Aa1234567890')
    login(request, user)
    return render(request, "back/index.html", locals())


@login_required(login_url=LOGIN_URL)
@csrf_exempt
def device_add(request):
    """
    :param request:
    :return:
    """
    device_add = True
    msg_ok = ""
    msg_err = ""

    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.api_key = (uuid.uuid4().hex)[:20] + (uuid.uuid4().hex)[:20]

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                f.remote_address = x_forwarded_for.split(',')[-1].strip()
            else:
                f.remote_address = request.META.get('REMOTE_ADDR') + "&" + request.META.get(
                    'HTTP_USER_AGENT') + "&" + request.META.get('SERVER_PROTOCOL')

            f.save()
            msg_ok = _(u'Add device successful, API key: ' + str(f.api_key) + '. Remember to store API key in a secret place!')
        else:
            msg_err = _(u'Error!')

    form = DeviceForm()

    return render(request, "back/add.html", locals())


@login_required(login_url=LOGIN_URL)
def device_list(request):
    """
    :param request:
    :return:
    """
    device_list = True
    list = Device.objects.all()
    return render(request, "back/device_list.html", locals())


@login_required(login_url=LOGIN_URL)
def device_edit(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Device, id=id)

    form = DeviceForm(request.POST or None, request.FILES or None, instance=val)
    if request.method == 'POST':
        if form.is_valid():
            change_status_to_device(val.api_key, id, form.cleaned_data["enable"])
            if form.cleaned_data["field_1"] != None:
                change_speed_to_device(val.api_key, id, form.cleaned_data["field_1"])
            form.save()
            msg_ok = _(u'Successfully edit device!')
            return HttpResponseRedirect(reverse('device_list'))
        else:
            msg_err = _(u'ERROR!')

    return render(request, "back/add.html", locals())


@login_required(login_url=LOGIN_URL)
def device_delete(request, id=None):
    """
    :param request:
    :param id:
    :return:
    """
    device = get_object_or_404(Device, id=id).delete()

    msg_ok = _(u'Successfully delete device')

    return HttpResponseRedirect(reverse('device_list'), locals())


@login_required(login_url=LOGIN_URL)
def key_list(request):
    """
    :param request:
    :return:
    """
    key_list = True
    list = Device.objects.filter(enable=True)
    return render(request, "back/key_list.html", locals())


@login_required(login_url=LOGIN_URL)
def generate_key(request, id=None):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Device, id=id)
    val.api_key = val.generate_key()
    val.save()
    list = Device.objects.filter(enable=True)
    msg_ok = _(u'Key üretildi')

    return HttpResponseRedirect(reverse('key_list'), locals())


# def export(request, model):
#     """
#     :param request:
#     :return:
#     """
#     model = apps.get_model(app_label=model + 's', model_name=model)
#     if request.GET['format'] == 'csv':
#         # Handle for csv file
#         response = HttpResponse(
#             content_type='text/csv',
#             headers={'Content-Disposition': 'attachment; filename="data.csv"'},
#         )
#
#         writer = csv.writer(response)
#         data = Data.objects.all()
#         writer.writerow(["Date", "Device", "Field_1", "Field_2", "Field_3", "Field_4", "Field_5", "Field_6",
#                          "Field_7", "Field_8", "Field_9", "Field_10"])
#         for entry in data:
#             writer.writerow([entry.pub_date, entry.device, entry.field_1, entry.field_2, entry.field_3,
#                              entry.field_4, entry.field_5, entry.field_6, entry.field_7, entry.field_8,
#                              entry.field_9, entry.field_10])
#
#         return response
#     else:
#         data = serializers.serialize(request.GET['format'], model.objects.all()[:100])
#
#     return JsonResponse({'response_data': data})

def change_status_to_device(api_key, device, status):
    client = PublicClient()
    # Repetition send packages
    client.send_command("ON" if status else "OFF", api_key, int(device))
    # client.send_command("ON" if status else "OFF", api_key, int(device))
    # client.send_command("ON" if status else "OFF", api_key, int(device))

def change_speed_to_device(api_key, device, speed):
    client = PublicClient()
    # Repetition send packages
    client.send_command("SPEED", api_key, int(device), speed=int(speed))
    # client.send_command("SPEED", api_key, int(device), speed=int(speed))
    # client.send_command("SPEED", api_key, int(device), speed=int(speed))
