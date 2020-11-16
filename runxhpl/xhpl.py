#!/usr/bin/env python3

"""
This module facilitates configuring and running the XHPL stress test.

    Typical Usage:

    my_xhpl = XHPL(mem_percent = 30)
    runs = my_xhpl.run_xhpl(num_runs = 10)
"""

import logging
import math
import numpy
import os
# import pkg_resources
import re
import statistics
import time

from engcommon import command
from engcommon import fileio
from engcommon import formattext
from engcommon import hardware
from engcommon import testvar

logger = logging.getLogger(__name__)


class XHPL:
    """A class for organsing and running XHPL for a specific platform.

    XHPL (High Performance Linpack) generates and solves a dense system
    of linear equations. It essentially takes a big matrix and breaks
    it into smaller pieces to be worked on in parallel.

    For best performance, choose the largest problem size (N) that will fit
    into memory. For QA purposes, the limit is typically 80% of installed memory.

    The resulting N x N matrix is "decomposed" into smaller blocks of size
    NB x NB that are then dealt onto the P x Q process grid. Results are
    checked by regenerating the input matrix and checking the error.

    https://www.netlib.org/benchmark/hpl/
    https://www.netlib.org/utk/people/JackDongarra/PAPERS/hpl.pdf
    https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/#hpl-main-parameters

    Attributes:
        mem_percent (int): Percentage of memory requested.
        num_cores (int): Number of cores.
        mem_free (int): Amount of free memory (kB).
        mem_xhpl (int): Amount of memory for XHPL (kB).
        P (int), Q (int): P x Q process matrix.
        NB (int): Block size.
        N (int): Problem size.
        hpl_dat (str): standard HPL.dat filled in with run parameters.
        cmd (str): XHPL command to run.
        status (str): XHPL run status.
        gflops_mean: Mean GFLOPs for runs.
        time_mean: Mean time (s) for runs.
    """

    def __init__(self, **kwargs):
        """Init XHPL.

        **kwargs:
            mem_percent (int): Percentage of memory requested.
        """
        if "mem_percent" not in kwargs.keys():
            try:
                raise TypeError("Missing keyword argument: 'mem_percent'")
            except TypeError:
                logger.error("Keyword Argument Missing Error")
                logger.debug(testvar.get_debug(kwargs))
                raise

        self._mem_percent = self._get_mem_percent(kwargs["mem_percent"])
        self._num_cores = self._get_num_cores()
        self._mem_free = self._get_mem_free()
        self._mem_xhpl = self._get_mem_xhpl()
        self._P, self._Q = self._get_PQ()
        self._NB = self._get_NB()
        self._N = self._get_N()
        self._hpl_dat = self._get_hpl_dat()
        self._cmd = self._get_xhpl_cmd()
        self._status = ""
        self._gflops_mean = None
        self._time_mean = None

    @property
    def mem_percent(self):
        "Get mem percent."
        return self._mem_percent

    @property
    def num_cores(self):
        "Get num cores."
        return self._num_cores

    @property
    def mem_xhpl(self):
        "Get XHPL mem."
        return self._mem_xhpl

    @property
    def N(self):
        "Get N."
        return self._N

    @property
    def NB(self):
        "Get NB."
        return self._NB

    @property
    def P(self):
        "Get P."
        return self._P

    @property
    def Q(self):
        "Get Q."
        return self._Q

    @property
    def hpl_dat(self):
        "Get HPL.dat."
        return self._hpl_dat

    @property
    def cmd(self):
        "Get XHPL cmd."
        return self._cmd

    @property
    def status(self):
        "Get XHPL run status."
        return self._status

    @property
    def gflops_mean(self):
        "Get mean GFLOPs."
        return self._gflops_mean

    @property
    def time_mean(self):
        "Get mean runtime."
        return self._time_mean

    def _get_mem_percent(self, mem_percent):
        try:
            int(mem_percent)
        except ValueError:
            logger.error("Invalid Integer Error")
            logger.debug(testvar.get_debug(mem_percent))
        return mem_percent

    def _get_num_runs(self, num_runs):
        try:
            int(num_runs)
        except ValueError:
            logger.error("Invalid Integer Error")
            logger.debug(testvar.get_debug(num_runs))
        return num_runs

    def _get_num_cores(self):
        return hardware.get_cpu_core_count()

    def _get_mem_free(self):
        kB = 1024
        return hardware.get_meminfo()["MemFree"] * kB

    def _get_mem_xhpl(self):
        return int(self._mem_free * self._mem_percent / 100)

    def _get_PQ(self):
        return get_PQ(self._num_cores)

    def _get_NB(self):
        return get_NB()

    def _get_N(self):
        """Get Problem size (N).

        Choose N such that: N % NB * LCM(P,Q) = 0

        Args:
            None

        Returns:
            N (int): Problem size.
        """
        N = int(math.sqrt(self._mem_xhpl / 8))
        divisor = self._NB * numpy.lcm(self._P, self._Q)
        N = (N // divisor) * divisor
        return N

    def _get_hpl_dat(self):
        """Get HPL.dat from template.

        Args:
            None

        Returns:
            hpl_dat (str): HPL.dat.
        """
        hpl_dat = get_hpl_dat_tmpl()
        hpl_dat = hpl_dat.replace(
            "%N%", "{0}".format(self._N)
        ).replace(
            "%NB%", "{0}".format(self._NB)
        ).replace(
            "%P%", "{0}".format(self._P)
        ).replace(
            "%Q%", "{0}".format(self._Q)
        )
        return hpl_dat

    def _get_xhpl_cmd(self):
        """Get XHPL command to run.

        Args:
            None

        Returns:
            cmd (str): XHPL command.
        """
        # The docker container uses IntelMPI. Otherwise the user is responsible
        # for MPI installation and $PATH resolution for mpirun.
        cmd_mpirun = "mpirun"
        arch = hardware.get_arch()
        if arch in ["x86_64"]:
            cmd_options = ""
        else:
            pass  # This POC only supports x86_64

        cmd_xhpl = "xhpl-{0}".format(arch)
        if hardware.get_cpu_vendor() == "intel":
            cmd_xhpl = "{0}-{1}".format(cmd_xhpl, get_xhpl_cpu_optimisations())

        cmd = "{0} {1} -np {2} {3}".format(
            cmd_mpirun,
            cmd_options,
            self._num_cores,
            cmd_xhpl,
        )
        return cmd

    def _run_xhpl(self, **kwargs):
        """Run XHPL and get output.

        Args:
            None

        **kwargs:
            runs (int): Number of runs. (required)

        Returns:
            runs_dict (dict): STDOUT of run keyed by run number.
        """

        if "num_runs" not in kwargs.keys():
            try:
                raise TypeError("Missing keyword argument: 'num_runs'")
            except TypeError:
                logger.error("Keyword Argument Missing Error")
                logger.debug(testvar.get_debug(kwargs))
                raise
        num_runs = self._get_num_runs(kwargs["num_runs"])

        GB = 1024 * 1024 * 1024
        logger.debug("CORES: {0}, MEM: {1} GB".format(
            self._num_cores,
            self._mem_free // GB,
        ))
        logger.debug("MEM_PERCENT: {0}, RUNS: {1}".format(
            self._mem_percent, num_runs
        ))
        logger.debug("MEM_XHPL: {0} GB".format(self._mem_xhpl // GB))
        logger.debug("Generating HPL.dat")

        # Write HPL.dat to the same dir as xhpl binary
#         xhpl_bin = pkg_resources.resource_stream(
#             __name__,
#             "bin/xhpl-{0}".format(hardware.get_arch()),
#         ).name
        regex_xhpl = r"xhpl-[a-zA-Z0-9_-]+"
        match = re.search(regex_xhpl, self.cmd)
        cmd_xhpl = m.groups()[0]
        dict_ = command.get_shell_cmd("which {0}".format(xhpl_bin))
        cmd_xhpl_path = dict_["stdout"].strip()
        xhpl_bin_dir = os.path.dirname(xhpl_bin)
        hpl_dat_filename = "{0}/HPL.dat".format(xhpl_bin_dir)
        logger.debug(testvar.get_debug({
            "N": self._N,
            "NB": self._NB,
            "P": self._P,
            "Q": self._Q,
        }))
        logger.debug("HPL.dat: {0}".format(hpl_dat_filename))
        fileio.write_file(hpl_dat_filename, self._hpl_dat, 'w')

        logger.debug(testvar.get_debug(self._cmd))
        logger.info("Starting XHPL")
        logger.info("{0:<11}{1:<8}{2:>4} {3:<10}{4:<10}".format(
            "STATUS", "TEST", "RUN", "TIME", "GFLOPS"
        ))
        status_runs = []
        gflops_runs = []
        time_runs = []
        count = 1
        while True:
            self._print_status(
                status = "STARTED",
                test_name = "xhpl",
                run = count,
            )
            try:
                dict_ = command.get_shell_cmd(self._cmd, cwd = xhpl_bin_dir)
            except KeyboardInterrupt:
                break
            else:
                (
                    passfail,
                    xhpl_time,
                    xhpl_gflops,
                ) = get_result(dict_["stdout"])
                status_runs.append(passfail)
                gflops_runs.append(float(xhpl_gflops))
                time_runs.append(float(xhpl_time))
                self._print_status(
                    status = passfail,
                    test_name = "xhpl",
                    run = count,
                    time = xhpl_time,
                    gflops = xhpl_gflops,
                )
                run_log = (
                    "--- stdout ---\n{0}\n".format(dict_["stdout"])
                    + "--- stderr ---\n{0}\n".format(dict_["stderr"])
                )
                runs_dict = {str(count): run_log}
            count += 1
            if (count > num_runs) and (num_runs != 0):
                break
            else:
                time.sleep(1)
        self._gflops_mean = statistics.mean(gflops_runs)
        self._time_mean = statistics.mean(time_runs)
        if not ("FAILED" or "ERROR") in status_runs:
            self._status = "PASSED"
        else:
            self._status = "FAILED"
        return runs_dict

    def run_xhpl(self, **kwargs):
        return self._run_xhpl(**kwargs)

    def _print_status(self, **kwargs):
        """Print status line of XHPL run.

        Args:
            None

        **kwargs:
            status (str): Status of run.
            test_name (str): Name of test.
            run (int): Run #.
            time (str): Duration of run.
            gflops (str): Performance of run.

        Returns:
            None
        """
        status = kwargs["status"]
        status_colour = {
            "STARTED": "bold",
            "PASSED": "green",
            "FAILED": "red",
            "ERROR": "yellow",
        }
        if status in ["STARTED", "FAILED", "ERROR"]:
            format_row = "{0:<20}{1:<8}{2:>4}"
            format_vars = (
                formattext.add_colour(status, status_colour[status]),
                kwargs["test_name"],
                "#" + str(kwargs["run"]),
            )
        elif status == "PASSED":
            format_row = "{0:<20}{1:<8}{2:>4} {3:<10}{4:<10}"
            format_vars = (
                formattext.add_colour(status, status_colour[status]),
                kwargs["test_name"],
                "#" + str(kwargs["run"]),
                kwargs["time"],
                kwargs["gflops"],
            )
        logger.info(format_row.format(*format_vars))
        return None


def get_result(stdout):
    """Get result of XHPL run.

    Args:
        stdout (str): STDOUT from XHPL run.

    Returns:
        tuple(
            status (str): Pass / fail status.
            xhpl_time (str): Duration of XHPL run.
            xhpl_gflops (str): Performance of XHPL run.
        )
    """
    # XHPL result is in stdout and looks like:

# ================================================================================
# T/V                N    NB     P     Q               Time                 Gflops
# --------------------------------------------------------------------------------
# WR00L2L2       55432   192     7     8            1831.58             6.1999e+01
# --------------------------------------------------------------------------------
# ||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   2.37118975e-03 ...... PASSED
# ================================================================================

    xhpl_time = ""
    xhpl_gflops = ""
    xhpl_status = ""
    # variant is the factorization algorithm (e.g. WR00L2L2)
    variant_regex = (
        r"\nWR[A-Z0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+\s+"
        r"([0-9.]+)\s+([0-9.e\+]+)"
    )
    match_0 = re.search(variant_regex, stdout)
    if match_0:
        xhpl_time = match_0.groups()[0]
        xhpl_gflops = match_0.groups()[1]

    error_expr = r"||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)="
    error_expr = re.escape(error_expr)
    match_1 = re.search(
        r"{0}\s+[0-9.e-]+\s+[\.]+\s+([A-Z]+)".format(error_expr),
        stdout,
    )
    if match_1:
        xhpl_status = match_1.groups()[0]

    if xhpl_status == 'PASSED':
        status = "PASSED"
    elif xhpl_status == 'FAILED':
        status = "FAILED"
    else:
        status = "ERROR"

    return (status, xhpl_time, xhpl_gflops)


def get_hpl_dat_tmpl():
    """Get HPL.dat template.

    Args:
        None

    Returns:
        hpl_dat_tmpl (str): HPL.dat template.
    """
    hpl_dat_tmpl = """
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
%N%        Ns
1            # of NBs
%NB%       NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
%P%        Ps
%Q%        Qs
16.0         threshold
1            # of panel fact
0            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
2            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
0            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
0            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
    """.strip()
    return hpl_dat_tmpl


def get_xhpl_cpu_optimisations():
    """Get XHPL CPU optimisations.

    Get the CPU SIMD for optimised XHPL.
    Currently only supports Intel processors.

    Args:
        None

    Returns:
        build_opt (str): CPU optimisation.
    """
    # https://software.intel.com/content/www/us/en/develop/articles/performance-tools-for-software-developers-intel-compiler-options-for-sse-generation-and-processor-specific-optimizations.html
    # https://en.wikipedia.org/wiki/Advanced_Vector_Extensions

    compiler_opts = {
        "core-avx512": [
            "avx512f",
            "avx512cd",
            "avx512dq",
            "avx512bw",
            "avx512vl",
            "avx2",
            "avx",
        ],
        "common-avx512": [
            "avx512f",
            "avx512cd",
            "avx2",
            "avx",
        ],
        "core-avx2": [
            "avx2",
            "avx",
        ],
        "core-avx-i": [
            "avx",
        ],
        "avx": [
            "avx",
        ]
    }

    build_opt = None
    avx_flags = hardware.get_cpu_flags_with_prefix("avx")
    for opt, instructions in compiler_opts.items():
        if set(instructions).issubset(set(avx_flags)):
            build_opt = opt
            break

    testvar.check_null(build_opt)  # Any modern Intel CPU has at least "avx"
    return build_opt


def get_xhpl_cpu_optimizations():
    return get_xhpl_cpu_optimisations()


def get_PQ(num_cores):
    """Get the process grid dimensions, PxQ.

    The process grid should be the most-square, non-square rectangle.

    Args:
        num_cores (int): Number of CPU cores.

    Returns:
        P (int): Grid dimension.
        Q (int): Grid dimension.
    """
    P = 1
    Q = (num_cores // P)
    diff = Q - P
    for i in range(P, Q):
        if (num_cores % i == 0):
            P_tmp = i
            Q_tmp = num_cores // i
            if (Q_tmp >= P_tmp):
                current_diff = Q_tmp - P_tmp
                if (current_diff < diff) and (current_diff > 0):
                    diff = current_diff
                    P = P_tmp
                    Q = Q_tmp
    return P, Q


def get_NB():
    """Get XHPL block size, NB.

    Args:
        None

    Returns:
        NB (int): Block size.
    """
    # https://github.com/pytorch/cpuinfo/blob/master/src/x86/uarch.c
    # https://software.intel.com/en-us/mkl-linux-developer-guide-configuring-parameters
    # http://developer.amd.com/wp-content/resources/56420.pdf
    # https://community.arm.com/developer/tools-software/hpc/b/hpc-blog/posts/profiling-and-tuning-linpack-step-step-guide

    vendor = hardware.get_cpu_vendor()
    cpuinfo = hardware.get_cpuinfo()
    cpu_family = int(cpuinfo[0]["cpu family"])
    cpu_model = int(cpuinfo[0]["model"])

    # CPU models
    # Intel (needs updates for newer procs)
    nehalem = {0x1a, 0x1e, 0x1f, 0x2e, 0x25}
    westmere = {0x2c, 0x2f}
    sandybridge = {0x2a, 0x2d}
    ivybridge = {0x3a, 0x3e}
    haswell = {0x3f, 0x45, 0x46}
    broadwell = {0x3d, 0x47, 0x4f, 0x56}
    skylake_client = {0x4e, 0x5e}
    skylake_server = {0x55}
    knightslanding = {0x57}

    # AMD
    bulldozer = {0x00, 0x01}
    zen = {0x01, 0x08, 0x11, 0x18}
    zen2 = {0x31, 0x60, 0x71}

    # ARM
    thunderx = {0x0a0, 0x0a1, 0x0a2, 0x0a3}
    thunderx2 = {0x0af}

    c = {None}
    NB = None
    if vendor == 'intel':
        if cpu_family == 0x06:
            if cpu_model in c.union(
                nehalem,
                westmere,
                sandybridge,
                ivybridge,
            ):
                NB = 256
            elif cpu_model in c.union(haswell, broadwell, skylake_client):
                NB = 192
            elif cpu_model in skylake_server:
                NB = 336
            elif cpu_model in knightslanding:
                NB = 384
    elif vendor == 'amd':
        if cpu_family == 0x15:
            if cpu_model in bulldozer:
                NB = 100
        if cpu_family == 0x16:
            if cpu_model in c.union(zen, zen2):
                NB = 232
    elif vendor == 'arm':
        if cpu_model in c.union(thunderx, thunderx2):
            NB = 128

    if not NB:
        NB = 192
    return NB
