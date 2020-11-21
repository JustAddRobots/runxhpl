Changelog
=========

0.1.4 (2020-11-21)
------------------
- Stage: Added misc fixes. (814ba7e) [JustAddRobots]
- Stage: Reverted changes, no 'make' in jenkins-docker, see ISSUE-010. (9505d18) [JustAddRobots]
- Stage: Added more shell troubleshooting. (352f722) [JustAddRobots]
- Stage: Added more make troubleshooting bits. (ee853cb) [JustAddRobots]
- Stage: Added jenkinslinter, but the pre-commit hook is broken. (740e037) [JustAddRobots]
- Stage: Added shell $PATH echo, jenkinslint. (a638591) [JustAddRobots]
- LOAD-010: Added echo of $PATH during build for troubleshooting. (3e280a7) [JustAddRobots]

0.1.1 (2020-11-16)
------------------
- Stage: Added repofile for epel, openblas. (e685db8) [JustAddRobots]
- Stage: Added epel-release for openblas-devel to Dockerfile. (879964a) [JustAddRobots]
- Stage: Fixed typo. (ffcb341) [JustAddRobots]
- Stage: Reverted to OpenMPI, OpenBLAS, un-optimised XHPL. (f5cf5c5) [JustAddRobots]
- Stage: Updated for full impi install tarball. (a7aab19) [JustAddRobots]
- Stage: Fixed xhpl_bin command path parsing. (b501b7e) [JustAddRobots]
- Stage: Added more mpiexec.hydra troubleshooting bits. (e6a17da) [JustAddRobots]
- Stage: Added troubleshooting for mpiexec. (d9c9f65) [JustAddRobots]
- Stage: Fixed typo. (4a3eff4) [JustAddRobots]
- Stage: Removed pkgresources since removal of xhpl bin, fixed opt order. (45f623f) [JustAddRobots]
- Stage: Fixed kwargs for num_runs. (c3119c3) [JustAddRobots]
- Stage: Fixed typo. (cbeb217) [JustAddRobots]
- Stage: Fixed mem_percent kwargs detection. (b629183) [JustAddRobots]
- Stage: Fixed typo for mem_percent kwarg. (21ea9a5) [JustAddRobots]
- Stage: Fixed rename of BURN constants. (ee73243) [JustAddRobots]
- Stage: Added fixes for docker build. (03832be) [JustAddRobots]
- ISSUE-005: Fixed Makefile escapes. (b6c8597) [JustAddRobots]
- ISSUE-005: Fixed misc typos. (236c604) [JustAddRobots]
- ISSUE-005: Removed bin/lib from manifest and setup.py. (66a7267) [JustAddRobots]
- ISSUE-005: Removed unnecessary runxhpl bin/lib. (398434c) [JustAddRobots]
- ISSUE-005: Activated pre-commit, added fixes. (c99548e) [JustAddRobots]
- ISSUE-005: Added XHPL Dockerfile and bin/lib. (7087c5a) [JustAddRobots]
- ISSUE-003: Activated pre-commit, added fixes. (ee218c2) [JustAddRobots]
- ISSUE-001: Added miscellaeous bits after util module removal. (b2575e1) [JustAddRobots]
- ISSUE-001: Removed util module references. (a46bbc9) [JustAddRobots]
- ISSUE-001: Adding more bits for rebuild/rewrite. (34c3c3b) [JustAddRobots]
- ISSUE-001: Added bits to start normalising POC. (bc18d61) [JustAddRobots]
- Initial commit. (a31cc46) [JustAddRobots]
