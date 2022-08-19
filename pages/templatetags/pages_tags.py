from config.context_processor import *
from django import template

from ..extensions.schedule_processing import *
from ..extensions.system_connector import *

register = template.Library()


@register.inclusion_tag('pages/private/function_module_1.html')
def current_system_status():
    status_data = {
        'host_power': host_power(),
        'site_status': site_status(),
        'ssh_function': ssh_function(),
        'ssh_connection_count': ssh_connection_count(),
        'local_ip_address': local_ip_address(),
        'global_ip_address': global_ip_address(),
        'ssh_port': ssh_port(),
        'ssh_max_simultaneous_connection_count': ssh_max_simultaneous_connection_count(),
    } | site_common_settings(None)
    return status_data


@register.inclusion_tag('pages/private/function_module_2.html')
def possible_management_actions():
    action_data = {
        'ssh_function_can_be_enabled': ssh_function() == 1,
        'ssh_function_can_be_disabled': ssh_function() == 2,
        'ssh_function_disable_reservation_is_filled': confirm_schedule_availability(process=1),
        'ssh_function_disable_reservation_waiting_time': get_schedule_waiting_time(process=1),
    } | site_common_settings(None)
    return action_data
