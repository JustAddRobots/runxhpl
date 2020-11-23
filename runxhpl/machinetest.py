#!/usr/bin/env python3


class XHPLTest:

    def __init__(self, *, name, cmd, start, end, params, metric, status, log):
        self._test_name = self._get_test_name(name)
        self._test_cmd = self._get_test_cmd(cmd)
        self._time_start = self._get_time_start(start)
        self._time_end = self._get_time_end(end)
        self._test_params = self._get_test_params(params)
        self._test_metric = self._get_test_metric(metric)
        self._test_status = self._get_test_status(status)
        self._test_log = self._get_test_log(log)

    @property
    def test_name(self):
        return self._test_name

    @property
    def test_cmd(self):
        return self._test_cmd

    @property
    def time_start(self):
        return self._time_start

    @property
    def time_end(self):
        return self._time_end

    @property
    def test_params(self):
        return self._test_params

    @property
    def test_metric(self):
        return self._test_metric

    @property
    def test_status(self):
        return self._test_status

    @property
    def test_log(self):
        return self._test_log

    def asdict(self):
        return {
            "test_name": self.test_name,
            "test_cmd": self.test_cmd,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "test_params": self.test_params,
            "test_metric": self.test_metric,
            "test_status": self.test_status,
            "test_log": self.test_log
        }

    def _get_test_name(self, name):
        return self._check_type(name, str)

    def _get_test_cmd(self, cmd):
        return self._check_type(cmd, str)

    def _get_time_start(self, start):
        return self._check_type(start, str)

    def _get_time_end(self, end):
        return self._check_type(end, str)

    def _get_test_params(self, params):
        return self._check_type(params, dict)

    def _get_test_metric(self, metric):
        return self._check_type(metric, str)

    def _get_test_status(self, status):
        return self._check_type(status, str)

    def _get_test_log(self, log):
        return self._check_type(log, str)

    def _check_type(self, var, var_type):
        if not isinstance(var, var_type):
            raise TypeError("{0} must be type {1}".format(var, var_type.__name))
        return var
