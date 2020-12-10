# runxhpl


## About

This repository contains tools for the configuration and execution of HPL (High 
Performance Linpack). It is meant more as a stress test for baremetal HPC computes, 
thus command-line options are geared toward multiple successive runs.

Please note that this repository currently executes the generic (**non-optimised**)
shared-memory benchmark.

One day maybe I'll include build tools for various compilers, BLAS, and MPI 
implementations in this repo.

There is **no support** for this project.


## Background

XHPL (High Performance Linpack) generates and solves a dense system of linear 
equations. It essentially takes a big matrix and breaks it into smaller pieces to 
be worked on in parallel.
    
For best performance, choose the largest problem size (N) that will fit into memory. 
The resulting N x N matrix is "decomposed" into smaller blocks of size NB x NB that 
are then dealt onto the P x Q process grid. Results are checked by regenerating the 
input matrix and checking the error.

For more information, see:
https://www.netlib.org/benchmark/hpl/
https://www.netlib.org/utk/people/JackDongarra/PAPERS/hpl.pdf
https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/HPL/#hpl-main-parameters


## Features

* Run XHPL with Targed Runs and Memory Usage
* Topology Query


## Installing



## Usage

```
usage: runxhpl [-h] [-d] [-l LOGID] [-m MEM] [-p PREFIX] [-r RUNS]
               [-u [UPLOAD]] [-v]

XHPL Stress Test

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           print debug information
  -l LOGID, --logid LOGID
                        force log_id (run identifier)
  -m MEM, --mem MEM     set memory percentage
  -p PREFIX, --prefix PREFIX
                        set prefix directory for logs
  -r RUNS, --runs RUNS  set number of runs
  -u [UPLOAD], --upload [UPLOAD]
                        upload to server
  -v, --version         show program's version number and exit

```


### Run HPL with targeted memory usage 

```
[root@hosaka /]# runxhpl --debug --mem 50 --runs 2 -u
2020-12-09 20:50:23 - INFO [clihelper]: runxhpl v: 0.6.0
2020-12-09 20:50:23 - DEBUG [clihelper]: engcommon v: 0.5.1
2020-12-09 20:50:23 - DEBUG [clihelper]: {'debug': True, 'dry_run': False, 'log_id': None, 'mem': 50, 'prefix': '/tmp/logs', 'runs': 2, 'upload': 'http://hosaka.local:3456/v1/machines'}
2020-12-09 20:50:23 - DEBUG [xhpl]: CORES: 4, MEM: 30 GB
2020-12-09 20:50:23 - DEBUG [xhpl]: MEM_PERCENT: 50, RUNS: 2
2020-12-09 20:50:23 - DEBUG [xhpl]: MEM_XHPL: 15 GB
2020-12-09 20:50:23 - DEBUG [xhpl]: Generating HPL.dat
2020-12-09 20:50:23 - DEBUG [xhpl]: {'N': 44352, 'NB': 336, 'P': 1, 'Q': 4}
2020-12-09 20:50:23 - DEBUG [xhpl]: HPL.dat: /usr/local/lib/python3.6/site-packages/runxhpl/bin/HPL.dat
2020-12-09 20:50:23 - DEBUG [xhpl]: 'mpirun --allow-run-as-root -mca btl_vader_single_copy_mechanism none -np 4 xhpl-x86_64'
2020-12-09 20:50:23 - INFO [xhpl]: Starting XHPL
2020-12-09 20:50:23 - INFO [xhpl]: STATUS     TEST     RUN TIME      GFLOPS
2020-12-09 20:50:23 - INFO [xhpl]: STARTED    xhpl      #1
2020-12-09 20:57:16 - INFO [xhpl]: PASSED     xhpl      #1 382.79    1.520e+02
2020-12-09 20:57:17 - INFO [xhpl]: STARTED    xhpl      #2
2020-12-09 21:04:03 - INFO [xhpl]: PASSED     xhpl      #2 379.12    1.534e+02
2020-12-09 21:04:03 - INFO [cli]: Status: PASSED
2020-12-09 21:04:03 - INFO [cli]: Mean Gflops: 152.7
2020-12-09 21:04:03 - INFO [clihelper]: LOGS: /tmp/logs/hosaka/serenely-canine-hindgut/runxhpl.2020.12.09-205023
2020-12-09 21:04:03 - INFO [cli]: Uploading to Database
2020-12-09 21:04:03 - DEBUG [connectionpool]: Starting new HTTP connection (1): hosaka.local:3456
2020-12-09 21:04:03 - DEBUG [connectionpool]: http://hosaka.local:3456 "POST /v1/machines HTTP/1.1" 200 0
2020-12-09 21:04:03 - INFO [cli]: Done.
``` 


### Topology Querying 

```
>>> myxhpl = xhpl.XHPL(mem_percent=80)
>>> myxhpl.N
56448
>>> myxhpl.NB
336
>>> myxhpl.cmd
'mpirun --allow-run-as-root -mca btl_vader_single_copy_mechanism none -np 4 xhpl-x86_64'
```

```
>>> xhpl.get_xhpl_cpu_optimizations()
'core-avx512'
>>> xhpl.get_PQ(96)
(8, 12)
```


## License

Licensed under GNU GPL v3. See **LICENSE.md**.
