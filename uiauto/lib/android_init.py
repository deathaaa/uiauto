import os
import sys
import time

from uiauto.util.android_util import AndroidUtil
from uiauto.util.file_util import FileUtil

__author__ = 'test'


class AndroidInit:
    def __init__(self):
        pass

    @staticmethod
    def init(appium_path, app_path, server_port, bootstrap_port, app_package, device_num, need_uninstall, need_install):
        if device_num == '':
            device_nums = AndroidUtil.get_device_nums()
            if len(device_nums) > 0:
                device_num = device_nums[0]
        copy_app_path = app_path.replace('.apk', '_%s.apk' % device_num)
        FileUtil.delete_file(copy_app_path)
        FileUtil.copy_file(app_path, copy_app_path)
        if need_install.lower() == 'true':
            if need_uninstall.lower() == 'true':
                print os.popen('adb -s %s %s %s' % (device_num, 'uninstall', app_package)).read()
            print os.popen('adb -s %s %s -r %s' % (device_num, 'install', app_path)).read()
        if sys.platform == 'darwin' or sys.platform == 'linux2':
            os.system('start_appium.sh %s %s %s %s %s &' % (
                appium_path, copy_app_path, device_num, server_port, bootstrap_port))
        else:
            os.system('start /b start_appium.bat %s %s %s %s %s' % (
                appium_path, copy_app_path, device_num, server_port, bootstrap_port))
        time.sleep(15)
