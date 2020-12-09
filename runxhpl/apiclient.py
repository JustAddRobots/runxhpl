#!/usr/bin/env python3

"""
This module is a minimal API client implementation. For XHPL tests we should only
create new logs for each test run. Therefore only the HTTP POST action is included.
READ should be done by a front-end app. UPDATE and DELETE should never automatically
be done for test logs.
"""

import json
import requests

from runxhpl import machinehardware
from runxhpl import machinetest


def post(my_cli, my_xhpl, upload_url, *, start, end, logs):
    """Post XHPL test run.

    Args:
        my_cli (clihelper.CLI): CLI helper instance.
        my_xhpl (xhpl.XHPL): XHPL test instance.
        upload_url (str): Upload logs to this URL.
        start (timestamp): Start time.
        end (timestamp): End time.
        logs (string): Test logs.

    Returns:
        status_code (int): HTTP status code.

    Raises:
        Exception: Error if HTTP status_code >= 400.
    """
    my_hardware = machinehardware.XHPLHardware()
    my_test = machinetest.XHPLTest(
        name = "xhpl",
        cmd = my_xhpl.cmd,
        start = start,
        end = end,
        params = {
            "N": my_xhpl.N,
            "NB": my_xhpl.NB,
            "P": my_xhpl.P,
            "Q": my_xhpl.Q
        },
        metric = my_xhpl.gflops_mean,
        status = my_xhpl.status,
        log = logs
    )

    # Prepare single dictionary for JSON conversion
    machines = {**my_hardware.asdict(), **my_test.asdict()}
    machines["log_id"] = my_cli.log_id
    machines_json = {
        "json": json.dumps(machines)
    }

    # Write to local logfile and upload to SQL DB
    my_cli.write_logs(machines_json, 'a')
    resp = requests.post(upload_url, json=machines)
    status_code = resp.status_code
    if status_code >= 400:
        raise requests.Exception("POST /machines/ {}".format(resp.status_code))
    return status_code
