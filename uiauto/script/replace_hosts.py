#!/usr/bin/env python
import getopt
import platform
import re
import sys

from uiauto.util.config_reader import ConfigReader


def replace_hosts(path, ip, host):
    replaced = 0
    count = 0
    re_str = r'^(\d+\.\d+\.\d+\.\d+)[\s\t]+%s' % host.replace('.', '\.')
    domain_re = re.compile(re_str)
    lines = file(path).readlines()
    for line in lines:
        m = domain_re.match(line)
        if m and not (replaced > 0):
            replaced += 1
            print ip, host
            lines[count] = ip + ' ' + host + '\r\n'
        else:
            print line.strip()
            lines[count] = line.strip() + '\r\n'
        count += 1

    if replaced == 0:
        print ip, host
        lines = lines + list(ip + ' ' + host + '\r\n')

    hostFile = open(path, 'w')
    hostFile.writelines(lines)
    hostFile.close()


def usage():
    print """
        Usage :
            -k, --key=       key
            -v, --value=     value
            -f, --file=      file
    """
    sys.exit()


def get_opt():
    try:
        options, args = getopt.getopt(sys.argv[1:], "k:v:f:", ["key=", "value=", "file="])
        opt = {}
        for option, arg in options:
            if option in ('-k', '--key'):
                opt['key'] = arg
            if option in ('-v', '--value'):
                opt['value'] = arg
            if option in ('-f', '--file'):
                opt['file'] = arg
        return opt['key'], opt['value'], opt['file']
    except:
        usage()


if '__main__' == __name__:
    # config_reader=ConfigReader(r'C:\Appium\qunar_case\conf\pc_beta.conf')
    option = get_opt()
    filename = option[2]
    config_reader = ConfigReader(filename)
    section = config_reader.read('host')
    ip = config_reader.read('ip', section)
    host = config_reader.read('host', section)
    if 'Windows' in platform.platform():
        replace_hosts('C:\\Windows\\System32\\drivers\\etc\\hosts', ip, host)
    else:
        replace_hosts('/etc/hosts', ip, host)
