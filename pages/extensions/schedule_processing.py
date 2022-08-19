import datetime
import threading

from django.db.utils import OperationalError, ProgrammingError

from ..models import ActionLog, AutomaticProcessingSchedule
from .simplemmap import simplemmap
from .system_connector import *

timer_dict = {}
mmap_client = simplemmap('./.mmap_1.dat')


def schedule_process(schedule_object):
    if 'schedule_object_' + str(schedule_object.pk) in timer_dict:
        cancel_scheduled_process(schedule_object)
    timer_dict['schedule_object_' + str(schedule_object.pk)] = threading.Timer((schedule_object.run_at - datetime.datetime.now()).total_seconds(), do_process, args=(schedule_object,))
    timer_dict['schedule_object_' + str(schedule_object.pk)].daemon = True
    timer_dict['schedule_object_' + str(schedule_object.pk)].start()


def cancel_scheduled_process(schedule_object):
    timer = timer_dict.pop('schedule_object_' + str(schedule_object.pk), None)
    if timer is not None:
        timer.cancel()


def do_process(schedule_object):
    timer = timer_dict.pop('schedule_object_' + str(schedule_object.pk), None)
    if timer is not None:
        timer.cancel()
    if schedule_object.process == 1:
        cmd = 'setting_ssh_function enabled=False\n'\
            'setting_ssh_service_auto_startup enabled=False'
        mmap_client.write_data(cmd.encode())
    logs = ActionLog.objects.filter(created_by=schedule_object.created_by, type=3, execution_time=schedule_object.run_at)
    if logs.exists() == True:
        logs[0].execution_time = datetime.datetime.now()
        logs[0].executed = True
        logs[0].save()
    schedule_object.delete()


def at_startup():
    ssh_function_status = ssh_function()
    ssh_service_auto_startup_status = ssh_service_auto_startup()
    if ssh_function_status == 1 and ssh_service_auto_startup_status == 1:
        setting_ssh_service_auto_startup(enabled=False)
    elif ssh_function_status == 2 and ssh_service_auto_startup_status == 0:
        setting_ssh_service_auto_startup(enabled=True)
    try:
        schedules = AutomaticProcessingSchedule.objects.all()
        if schedules.exists() == True:
            for schedule in schedules:
                schedule_process(schedule)
    except (OperationalError, ProgrammingError):
        pass


def register_schedule(created_by, process, run_at):
    if AutomaticProcessingSchedule.objects.filter(process=process).exists() == True:
        raise Exception()
    else:
        schedule = AutomaticProcessingSchedule.objects.create(created_by=created_by, process=process, run_at=run_at)
        schedule_process(schedule)
        ActionLog.objects.create(created_by=created_by, type=3, execution_time=schedule.run_at)


def unregister_schedule(created_by, process):
    schedules = AutomaticProcessingSchedule.objects.filter(created_by=created_by, process=process)
    if schedules.exists() == True:
        cancel_scheduled_process(schedules[0])
        logs = ActionLog.objects.filter(created_by=created_by, type=3, execution_time=schedules[0].run_at)
        if logs.exists() == True:
            log = logs[0]
            log.executed = False
            log.save()
        schedules[0].delete()
    else:
        raise Exception()


def confirm_schedule_availability(process):
    return AutomaticProcessingSchedule.objects.filter(process=process).exists()


def get_schedule_waiting_time(process):
    schedules = AutomaticProcessingSchedule.objects.filter(process=process)
    if schedules.exists() == True:
        return round((datetime.datetime.now() - schedules[0].run_at) / datetime.timedelta(hours=1))
    else:
        return None


at_startup()
