# -*- coding: utf-8 -*-
from uiauto.lib.android_monitor import AndroidMonitor
from uiauto.lib.ios_monitor import IosMonitor
from uiauto.lib.pc_chrome_monitor import PCChromeMonitor
from uiauto.lib.pc_firefox_monitor import PCFirefoxMonitor
from uiauto.lib.pc_ie_monitor import PCIEMonitor
from uiauto.lib.platform import PLATFORM
from uiauto.module.android_config import AndroidConfig
from uiauto.module.ios_config import IosConfig
from uiauto.module.pc_config import PCConfig

__author__ = 'litang.wang'


class Relation:
    def __init__(self, monitor_class, config_class):
        self.monitor_class = monitor_class
        self.config_class = config_class


monitor_relation = {
    PLATFORM.PC_CHROME: Relation(PCChromeMonitor, PCConfig),
    PLATFORM.PC_IE: Relation(PCIEMonitor, PCConfig),
    PLATFORM.PC_FIREFOX: Relation(PCFirefoxMonitor, PCConfig),
    PLATFORM.TOUCH: Relation(PCChromeMonitor, PCConfig),
    PLATFORM.ANDROID: Relation(AndroidMonitor, AndroidConfig),
    PLATFORM.IOS: Relation(IosMonitor, IosConfig),
}
