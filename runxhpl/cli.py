#!/usr/bin/env python3

"""
This module is the CLI front-end for the standardised XHPL Stress Test.
"""

import argparse
import logging
import os
import pkg_resources
import sys
import time

from engcommon import clihelper
from engcommon import ini
from engcommon import formattext
from engcommon import log
from engcommon.constants import _const as CONSTANTS
from runxhpl import apiclient
from runxhpl import xhpl


def get_command(args):
    """Get command args.

    Args:
        args (list): Argument list (e.g. sys.argv[1:]).

    Returns:
        args (dict): Arguments.
    """
    parser = argparse.ArgumentParser(
        description = "XHPL Stress Test"
    )
    parser.add_argument(
        "-d", "--debug",
        action = "store_true",
        help = "print debug information",
    )
    parser.add_argument(
        "-l", "--logid",
        action = "store",
        type = str,
        help = "force runtime log indentifier",
        required = False,
    )
    parser.add_argument(
        "-m", "--mem",
        action = "store",
        type = int,
        default = CONSTANTS().XHPL_MEM_PCT,
        help = "set memory percentage",
    )
    parser.add_argument(
        "-p", "--prefix",
        action = "store",
        type = str,
        default = "/tmp/logs",
        help = "set log directory prefix",
    )
    parser.add_argument(
        "-r", "--runs",
        action = "store",
        type = int,
        default = 0,  # infinite
        help = "set number of runs",
    )
    parser.add_argument(
        "-u", "--upload",
        action = "store",
        type = str,
        const = ini.INIConfig(CONSTANTS().INI_URL).xhplconsole_url,
        nargs = "?",
        help = "upload to server with URL",
    )
    parser.add_argument(
        "-v", "--version",
        action = "version",
        version = pkg_resources.get_distribution(parser.prog).version
    )
    args = vars(parser.parse_args(args))
    return args


# Run module code using input dict
def run(args):
    """Run.

    Args:
        args (dict): CLI Arguments.

    Returns:
        None
    """
    # Standardised CLI bits
    project_name = (os.path.dirname(__file__).split("/")[-1])
    my_cli = clihelper.CLI(project_name, args)
    logger = my_cli.logger
    my_cli.print_versions()

    mem_pct = args["mem"]
    runs = args["runs"]
    upload_url = args["upload"]

    my_xhpl = xhpl.XHPL(mem_percent = mem_pct)

    # Run XHPL
    time_start = time.strftime("%Y-%m-%d %H:%M:%S")
    runs_dict = my_xhpl.run_xhpl(num_runs = runs)
    time_end = time.strftime("%Y-%m-%d %H:%M:%S")

    # Show logs
    logger.info("{0}: {1}".format(
        formattext.add_colour("Status", "yellow"),
        my_xhpl.status,
    ))
    logger.info("Mean Gflops: {0}".format(my_xhpl.gflops_mean))
    my_cli.write_logs(runs_dict, "w")
    runs_blob = log.get_formatted_logs(runs_dict)
    my_cli.print_logdir()

    if upload_url:
        # Upload via API client
        logger.info("Uploading to Database")
        apiclient.post(
            my_cli,
            my_xhpl,
            upload_url,
            start=time_start,
            end=time_end,
            logs=runs_blob
        )

    logger.info("Done.\n")
    return None


def main():
    args = sys.argv[1:]
    d = get_command(args)
    run(d)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Exceptions Found")
        logging.critical("Exiting.")
        sys.exit()
