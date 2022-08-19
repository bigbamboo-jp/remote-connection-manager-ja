#!/usr/bin/env python
import os
import sys

import pages.extensions.simplemmap
import pages.extensions.system_connector


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'standby':
            subcommand_standby()
            return
        print('Error: Specified subcommand does not exist.')
    else:
        print('Error: Please specify a subcommand.')


def subcommand_standby():
    if os.geteuid() != 0:
        print('Error: This subcommand must be executed with root privileges.')
        return
    mmap_client = pages.extensions.simplemmap.simplemmap('./.mmap_1.dat')
    os.chmod('./.mmap_1.dat', 0o666)
    mmap_client.write_data(b'')
    print('Standby for communication from the main application.\nStop this module with CONTROL-C.')
    try:
        while True:
            if mmap_client.read_data() != b'':
                for command in mmap_client.read_data().decode().split('\n'):
                    try:
                        command_information = command.split(' ')
                        if command_information[0] == 'setting_ssh_function':
                            if command_information[1] == 'True' or command_information[1] == 'enabled=True':
                                pages.extensions.system_connector.setting_ssh_function(enabled=True)
                            elif command_information[1] == 'False' or command_information[1] == 'enabled=False':
                                pages.extensions.system_connector.setting_ssh_function(enabled=False)
                        elif command_information[0] == 'setting_ssh_service_auto_startup':
                            if command_information[1] == 'True' or command_information[1] == 'enabled=True':
                                pages.extensions.system_connector.setting_ssh_service_auto_startup(enabled=True)
                            elif command_information[1] == 'False' or command_information[1] == 'enabled=False':
                                pages.extensions.system_connector.setting_ssh_service_auto_startup(enabled=False)
                    except Exception as e:
                        # raise e
                        pass
                mmap_client.write_data(b'')
    except KeyboardInterrupt:
        mmap_client.dispose(leave_file=True)


if __name__ == '__main__':
    main()
