import os
import socket
import subprocess

import requests

try:
    from django.conf import settings
except ModuleNotFoundError:
    pass
# JSON形式のレスポンスを返すサービスのみ使用できる
PUBLIC_IP_ADDRESS_API_SETTINGS = ['https://httpbin.org/ip', 'origin']


def host_power():
    return 1


def site_status():
    if getattr(settings, 'DEBUG', False) == True:
        return 1
    else:
        return 0


def ssh_function():
    cmd = subprocess.run(['systemctl', 'status', 'sshd.service'], capture_output=True, text=True)
    if cmd.returncode == 4:
        cmd = subprocess.run(['systemctl', 'status', 'ssh.service'], capture_output=True, text=True)
    if 'Active: inactive' in cmd.stdout:
        return 1
    elif 'Active: active' in cmd.stdout:
        return 2
    else:
        return 0


def ssh_service_auto_startup():
    if os.path.isfile('/etc/systemd/system/multi-user.target.wants/sshd.service') == True or os.path.isfile('/etc/systemd/system/multi-user.target.wants/ssh.service') == True:
        return 1
    else:
        return 0


def ssh_connection_count():
    cmd1 = subprocess.Popen(['ss'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cmd2 = subprocess.run(['grep', '-i', 'ssh'], stdin=cmd1.stdout, capture_output=True, text=True)
    return len(cmd2.stdout)


def local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception as e:
        # raise e
        IP = None
    finally:
        s.close()
    return IP


def global_ip_address():
    try:
        res = requests.get(PUBLIC_IP_ADDRESS_API_SETTINGS[0])
        json_res = res.json()
        return json_res[PUBLIC_IP_ADDRESS_API_SETTINGS[1]]
    except Exception as e:
        # raise e
        return None


def ssh_port():
    cmd = subprocess.run(['grep', 'Port ', '/etc/ssh/sshd_config'], capture_output=True, text=True)
    for line in cmd.stdout:
        if line.startswith('Port ') == True:
            return int(line[len('Port '):])
    return 22  # 22 → デフォルトのSSH接続ポート


def ssh_max_simultaneous_connection_count():
    cmd = subprocess.run(['grep', 'MaxSessions ', '/etc/ssh/sshd_config'], capture_output=True, text=True)
    for line in cmd.stdout:
        if line.startswith('MaxSessions ') == True:
            return int(line[len('MaxSessions '):])
    return 10  # 10 → デフォルトのSSH最大同時接続数


def setting_ssh_function(enabled):
    if enabled == True:
        set_value = 'start'
    else:
        set_value = 'stop'
    cmd = subprocess.run(['systemctl', set_value, 'sshd.service'], capture_output=True, text=True)
    if cmd.returncode == 5:
        cmd = subprocess.run(['systemctl', set_value, 'ssh.service'], capture_output=True, text=True)
    if cmd.returncode == 0:
        return 0
    else:
        return 1


def setting_ssh_service_auto_startup(enabled):
    if enabled == True:
        set_value = 'enable'
    else:
        set_value = 'disable'
    cmd = subprocess.run(['systemctl', set_value, 'sshd.service'], capture_output=True, text=True)
    if cmd.returncode == 1:
        cmd = subprocess.run(['systemctl', set_value, 'ssh.service'], capture_output=True, text=True)
    if cmd.returncode == 0:
        return 0
    else:
        return 1
