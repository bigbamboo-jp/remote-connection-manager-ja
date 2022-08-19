import datetime

from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .extensions.schedule_processing import (confirm_schedule_availability,
                                             mmap_client, register_schedule,
                                             unregister_schedule)
from .models import ActionLog

# Create your views here.

SHOW_TERMS_OF_USE = getattr(settings, 'SHOW_TERMS_OF_USE', True)
SHOW_PRIVACY_POLICY = getattr(settings, 'SHOW_PRIVACY_POLICY', True)


def home(request):
    if request.user.is_authenticated == True:
        return render(request, 'pages/private/home.html')
    else:
        return render(request, 'pages/public/home.html')


def terms(request):
    if SHOW_TERMS_OF_USE == True:
        return render(request, 'pages/public/terms.html')
    else:
        return redirect('home')


def privacy_policy(request):
    if SHOW_PRIVACY_POLICY == True:
        return render(request, 'pages/public/privacy_policy.html')
    else:
        return redirect('home')


@require_POST
def action_ssh_function_enable(request):
    cmd = 'setting_ssh_function enabled=True\n'\
        'setting_ssh_service_auto_startup enabled=True'
    mmap_client.write_data(cmd.encode())
    log = ActionLog.objects.create(created_by=request.user, type=0, executed=True)
    log.execution_time = log.created_at
    log.save()
    return redirect('home')


@require_POST
def action_ssh_function_disable(request):
    try:
        unregister_schedule(request.user, 1)
    except Exception as e:
        # raise e
        pass
    if confirm_schedule_availability(1) == False:
        cmd = 'setting_ssh_function enabled=False\n'\
            'setting_ssh_service_auto_startup enabled=False'
        mmap_client.write_data(cmd.encode())
        log = ActionLog.objects.create(created_by=request.user, type=1, executed=True)
        log.execution_time = log.created_at
        log.save()
    return redirect('home')


@require_POST
def action_ssh_function_disable_reservation_register(request):
    try:
        register_schedule(request.user, 1, datetime.datetime.now() + datetime.timedelta(hours=float(request.POST['parameter-1'])))
    except Exception as e:
        # raise e
        pass
    return redirect('home')


@require_POST
def action_ssh_function_disable_reservation_unregister(request):
    try:
        unregister_schedule(request.user, 1)
    except Exception as e:
        # raise e
        pass
    return redirect('home')
