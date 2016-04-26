# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
        name='uiauto-framework',
        version='1.2.9',
        packages=[
            'uiauto',
            'uiauto.lib',
            'uiauto.util',
            'uiauto.annotation',
            'uiauto.module'
        ],
        scripts=[
            'uiauto/script/android_prepare.sh',
            'uiauto/script/android_prepare.bat',
            'uiauto/script/change_config.py',
            'uiauto/script/check_resfile.py',
            'uiauto/script/download_apk.py',
            'uiauto/script/ios_init.sh',
            'uiauto/script/killport.bat',
            'uiauto/script/record_client.py',
            'uiauto/script/replace_hosts.py',
            'uiauto/script/start_appium.bat',
            'uiauto/script/start_appium.sh',
            'uiauto/script/start_appium_for_ios.sh',
            'uiauto/script/upgrade.bat',
            'uiauto/script/upgrade.py'
        ],
        url='git@github.com:deathaaa/uiauto.git',
        license='',
        author='litang.wang',
        author_email='litang.wang@qunar.com',
        description='ui自动化框架',
        requires=[
            'selenium'
        ],
)
