#!/usr/bin/env python3

"""
This module module consolidates machine hardware information for logging
and export.
"""

from engcommon import hardware


class XHPLHardware:
    """A class for organising machine hardware information.

    Attributes:
        serial_num (string): serial number.
        uuid (string): UUID.
        cpu_vendor (string): CPU vendor.
        cpu_family_model_stepping (string): CPU spec (space separated).
        cpu_core_count (int): Total cores.
        cpu_flags (string): CPU flags enabled.
        lscpu (dict): 'lscpu'.
        cpuinfo (list): 'cpuinfo'.
        meminfo (dict): 'meminfo'.
    """
    def __init__(self):
        self._serial_num = self._get_serial_num()
        self._uuid = self._get_uuid()
        self._cpu_vendor = self._get_cpu_vendor()
        self._cpu_family_model_stepping = self._get_cpu_family_model_stepping()
        self._cpu_core_count = self._get_cpu_core_count()
        self._cpu_flags = self._get_cpu_flags()
        self._lscpu = self._get_lscpu()
        self._cpuinfo = self._get_cpuinfo()
        self._dmidecode = self._get_dmidecode()
        self._meminfo = self._get_meminfo()

    @property
    def serial_num(self):
        return self._serial_num

    @property
    def uuid(self):
        return self._uuid

    @property
    def cpu_vendor(self):
        return self._cpu_vendor

    @property
    def cpu_family_model_stepping(self):
        return self._cpu_family_model_stepping

    @property
    def cpu_core_count(self):
        return self._cpu_core_count

    @property
    def cpu_flags(self):
        return self._cpu_flags

    @property
    def lscpu(self):
        return self._lscpu

    @property
    def cpuinfo(self):
        return self._cpuinfo

    @property
    def dmidecode(self):
        return self._dmidecode

    @property
    def meminfo(self):
        return self._meminfo

    def asdict(self):
        return {
            "serial_num": self.serial_num,
            "uuid": self.uuid,
            "cpu_vendor": self.cpu_vendor,
            "cpu_family_model_stepping": self.cpu_family_model_stepping,
            "cpu_core_count": self.cpu_core_count,
            "cpu_flags": self.cpu_flags,
            "lscpu": self.lscpu,
            "cpuinfo": self.cpuinfo,
            "dmidecode": self.dmidecode,
            "meminfo": self.meminfo
        }

    def _get_serial_num(self):
        return hardware.get_serial_num()

    def _get_uuid(self):
        return hardware.get_uuid()

    def _get_cpu_vendor(self):
        return hardware.get_cpu_vendor()

    def _get_cpu_family_model_stepping(self):
        proc = hardware.get_cpuinfo()[0]
        family = proc["cpu family"]
        model = proc["model"]
        stepping = proc["stepping"]
        return "{0} {1} {2}".format(family, model, stepping)

    def _get_cpu_core_count(self):
        return hardware.get_cpu_core_count()

    def _get_cpu_flags(self):
        return hardware.get_cpuinfo()[0]["flags"]

    def _get_lscpu(self):
        return hardware.get_lscpu()

    def _get_cpuinfo(self):
        return hardware.get_cpuinfo()

    def _get_dmidecode(self):
        return hardware.get_dmidecode()

    def _get_meminfo(self):
        return hardware.get_meminfo()
