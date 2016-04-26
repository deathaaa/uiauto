# -*- coding: utf-8 -*-
import os
import re
import urllib

from uiauto.util.config_reader import ConfigReader

__author__ = 'litang.wang'


class UpgradeFramework:
    def __init__(self):
        pass

    @staticmethod
    def upgrade(auto_upgrade):
        infos = os.popen('pip show uiauto-framework').readlines()
        current_version = '0.0.0'
        for info in infos:
            m = re.match('^Version:\s+(\d+\.\d+\.\d+)', info)
            if m is not None:
                current_version = m.groups()[0]

        url = 'http://gitlab.corp.qunar.com/des-qa/uiauto_framework/raw/rb1/dist/release_record'
        lines = urllib.urlopen(url).readlines()
        new_version = None
        for line in lines:
            if re.match('^version:\s*%s' % current_version, line) is not None:
                break

            if new_version is None:
                m = re.match('^last_release_version:\s*(\d+\.\d+\.\d+)', line)
                if m is not None:
                    new_version = m.groups()[0]
                    print'new_version:%s;current_version:%s' % (current_version, new_version)
            else:
                print line[:-1]

        if current_version != new_version and new_version is not None:
            cmd = 'pip install --upgrade http://gitlab.corp.qunar.com/des-qa/uiauto_framework/raw/rb1/dist/uiauto-framework-%s.tar.gz' % new_version
            if auto_upgrade:
                os.system(cmd)
                exit(0)
            else:
                print 'new version is available ,please run command \"%s\" to upgarde.' % cmd

    @staticmethod
    def auto_upgrade(conf):
        config_reader = ConfigReader(conf)
        auto_upgrade = config_reader.read('auto_upgrade', 'config', 'true').lower()
        if auto_upgrade == 'true':
            UpgradeFramework.upgrade(True)
        else:
            UpgradeFramework.upgrade(False)


if __name__ == '__main__':
    UpgradeFramework.upgrade(True)
