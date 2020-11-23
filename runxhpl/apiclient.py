#!/usr/bin/env python3

# import requests

from runxhpl import machinehardware
from runxhpl import machinetest


def post(my_cli, my_xhpl, *, time_start, time_end, run_logs):
    my_hardware = machinehardware.XHPLHardware()
    my_test = machinetest.XHPLTest(
        name = "xhpl",
        cmd = my_xhpl.cmd,
        start = time_start,
        end = time_end,
        params = {
            "N": my_xhpl.N,
            "NB": my_xhpl.NB,
            "P": my_xhpl.P,
            "Q": my_xhpl.Q
        },
        metric = my_xhpl.gflops_mean,
        status = my_xhpl.status,
        log = run_logs
    )

    machines = {**my_hardware.asdict(), **my_test.asdict()}
    machines["log_id"] = my_cli.log_id
    my_cli.write_logs(machines, 'a')
#     resp = requests.post("http://hosaka.local:3456/machines/", json=machines)
#     if resp.status_code != 201:
#         raise ApiError("POST /machines/ {}".format(resp.status_code))
