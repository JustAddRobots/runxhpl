Changelog
=========

0.10.4 (2020-12-19)
-------------------
- ISSUE-076: Changed colour for demo. (5b0d5e2) [JustAddRobots]

0.10.3 (2020-12-19)
-------------------
- ISSUE-076: Changed colour for demo. (e9d866c) [JustAddRobots]

0.10.2 (2020-12-18)
-------------------
- ISSUE-076: Changed colour for demo. (0e10267) [JustAddRobots]

0.10.0 (2020-12-17)
-------------------
- ISSUE-072: Added upload CLI option. (6f8d199) [JustAddRobots]

0.9.3 (2020-12-16)
------------------
- ISSUE-068: Added echo stdout for float conversion error. (00b3b8b) [JustAddRobots]
- ISSUE-069: Disabled delete tags stage. (b1bdcea) [JustAddRobots]

0.9.1 (2020-12-14)
------------------
- ISSUE-061: Updated to a proper install of git inside docker build. (072f257) [JustAddRobots]

0.9.0 (2020-12-14)
------------------
- Stage: Added runxhpl @ git+https for Docker build. (5501295) [JustAddRobots]
- ISSUE-061: Updated for setup for engcommon @ git+https. (61ea5d7) [JustAddRobots]
- Stage: Fixed typo. (cc0c1e5) [JustAddRobots]
- Stage: Added repo explicitly. (0d9f9df) [JustAddRobots]
- Stage: Testing withCredentials tag delete push with USER/PW line. (3069865) [JustAddRobots]
- Stage: Switched delete tags stage back on + sshagent. (ede38f5) [JustAddRobots]
- Stage: Troubleshooting credentials. (72ff2d9) [JustAddRobots]
- Stage: Switched to sshagent plugin for tag delete. (0b4a149) [JustAddRobots]
- Stage: Fixed syntax in withCredentials. (c16726e) [JustAddRobots]
- Stage: Fixed incorrect var name. (cb554c4) [JustAddRobots]
- Stage: Added user/pw env vars to withCredentials delete tag stage. (149333e) [JustAddRobots]
- Stage: Added more syntax fixes. (7ea46e8) [JustAddRobots]
- Stage: Fixed syntax. (620a9e9) [JustAddRobots]
- Stage: Fixed syntax error. (5ae451b) [JustAddRobots]
- Stage: Added withCredentials for tag delete. (3fb3784) [JustAddRobots]
- Stage: Fixed typo in MMP interpolation. (a5c2ddb) [JustAddRobots]
- Stage: More troubleshooting MMP resolution. (a0568ac) [JustAddRobots]
- Stage: Troubleshooting env.MMP resolution for auto tag delete. (151ebaf) [JustAddRobots]
- Stage: Added vars to env. (5ec193a) [JustAddRobots]
- Stage: Troubleshooting MMP resolution. (8823393) [JustAddRobots]
- Stage: More pipeline fuckery. (20ce788) [JustAddRobots]
- Stage: More troubleshooting tag delete. (336beac) [JustAddRobots]
- Stage: Trouble shooting tag delete. (deafd08) [JustAddRobots]
- Stage: Fixed tag delete syntax, ordering. (2d3e15b) [JustAddRobots]
- Stage: Added echo of MMP for delete tag troubleshooting. (280d66f) [JustAddRobots]
- Stage: More Troubleshooting delete RC tags stage. (622a8a4) [JustAddRobots]

0.8.0 (2020-12-12)
------------------
- Stage: Troubleshooting "when" branch conditional. (db7a784) [JustAddRobots]
- Stage: Fixed syntax error. (ace7ba7) [JustAddRobots]
- Stage: Removed errant curly brace. (8790ba5) [JustAddRobots]
- Stage: Fixed escape of dollar sign in Jenkins pipeline "sh" (bbfa0cc) [JustAddRobots]
- ISSUE-043: Added make default & delete RC pipeline stages. (f738b66) [JustAddRobots]
- ISSUE-040: Updated to use INI_URL. (43e3ba4) [JustAddRobots]
- ISSUE-043: Added make default & delete RC pipeline stages. (7e36a11) [JustAddRobots]
- ISSUE-040: Updated to use INI_URL. (28caf9f) [JustAddRobots]

0.7.3 (2020-12-11)
------------------
- ISSUE-040: Updated to use INI_URL. (1379dfc) [JustAddRobots]
- ISSUE-040: Updated to use INI_URL. (399466b) [JustAddRobots]

0.7.0 (2020-12-10)
------------------
- ISSUE-034: Fixed link spacing. (64ef0a6) [JustAddRobots]
- ISSUE-034: Fixed misc language, bits. (276c952) [JustAddRobots]
- ISSUE-034: Added docs. (8b3c502) [JustAddRobots]
- ISSUE-031: Cleaned up CLI options. (16f5a58) [JustAddRobots]

0.6.0 (2020-12-10)
------------------
- Stage: Updated for JSON INI URL. (56e3ffc) [JustAddRobots]
- Stage: Troubleshooting env var access. (e1c09cb) [JustAddRobots]
- Stage: Added imperative env reference. (5fa3183) [JustAddRobots]
- Stage: Added props echo. (f5fcae1) [JustAddRobots]
- Stage: Added readProperties after readJSON. (68733ae) [JustAddRobots]
- Stage: Removed readJSON from env block. (905ea09) [JustAddRobots]
- Stage: More troubleshooting readJSON. (1d5ed07) [JustAddRobots]
- Stage: Added separate INI stage. (818d0ee) [JustAddRobots]
- Stage: Added readJSON directly to env block. (deaf58f) [JustAddRobots]
- Stage: Moved loadPropertiest to env block. (89002fd) [JustAddRobots]
- Stage: Troubleshooting readJSON for loadProperties() (5acb189) [JustAddRobots]
- Stage: Fixed quotes for var interpolation. (e7ceba8) [JustAddRobots]
- Stage: Fixed JSON string. (c762ebf) [JustAddRobots]
- Stage: Punted on INI format, switched to JSON for loadProperties. (2ffd077) [JustAddRobots]
- Stage: Troubleshooting loadProperties string -> map. (45b51dc) [JustAddRobots]
- Stage: Troubleshooting readProperties instantiaion with INI section name. (df60990) [JustAddRobots]
- Stage: Troubleshooting INI url download for Jenkins properties. (b91211b) [JustAddRobots]
- Stage: Added httpRequest module for INI url. (abca182) [JustAddRobots]
- Stage: Updated loadProperties() (d42e617) [JustAddRobots]
- Stage: Added loadProperties() (f1ba153) [JustAddRobots]
- Stage: Added loadProperties() with workaround until INI URL. (ef7b551) [JustAddRobots]
- ISSUE-030: Added INI config integration, option DB upload. (b916198) [JustAddRobots]

0.5.0 (2020-12-06)
------------------
- ISSUE-023: Fixed pre-commit options for non-test files. (6147469) [JustAddRobots]
- ISSUE-023: Remove setup.py for pytest error fix. (da06db8) [JustAddRobots]

0.4.0 (2020-12-06)
------------------
- Stage: Changed to ARG for ENGCOMMON_BRANCH. (d78add8) [JustAddRobots]
- Stage: Troubleshooting ENGCOMMON_BRANCH resoultion. (9c47955) [JustAddRobots]
- ISSUE-024: Added ENGCOMMON_BRANCH selector. (686e0fb) [JustAddRobots]

0.3.1 (2020-12-05)
------------------
- Stage: Removed property from machinetest.asdict. (266a8a6) [JustAddRobots]
- Stage: Removed unnecessary property decorator from asdict() (a6e252a) [JustAddRobots]
- Stage: Updated API status_code exception, machine classes. (4f24b15) [JustAddRobots]
- Stage: Updated HTTP status_code check >=400 until API update. (f6cf767) [JustAddRobots]
- Stage: Updated URL for versioned API. (5d2f27d) [JustAddRobots]
- Stage: Fixed syntax error. (6996749) [JustAddRobots]
- Stage: Added json dump to file for reuse/troubleshooting. (a01c395) [JustAddRobots]
- Stage: Changed N to int, might have been numpy int64. (7eb222d) [JustAddRobots]
- Stage: Added requests exception. (63df4f9) [JustAddRobots]

0.3.0 (2020-11-24)
------------------
- Stage: Fixed creation/addition of stdout/stderr to logs. (2ff11e9) [JustAddRobots]
- Stage: Fixed mistake of forgotten meminfo function. (fa3910a) [JustAddRobots]
- Stage: Changed metric back to str for MySQL storage. (5abf84b) [JustAddRobots]
- Stage: Changed metric type to float. (71d8d02) [JustAddRobots]
- Stage: Fixed typo. (b190ffb) [JustAddRobots]
- Stage: Added missing time_end function. (74e531f) [JustAddRobots]
- Stage: Fixed typo. (3bd565a) [JustAddRobots]
- Stage: Fixed typo. (d433dcc) [JustAddRobots]
- Stage: Fixed typo. (d722691) [JustAddRobots]
- Stage: Fixed typo. (6898544) [JustAddRobots]
- Stage: Fixed typo. (15730f3) [JustAddRobots]
- Stage: Added dmidecode to Dockerfile. (d80276d) [JustAddRobots]
- Stage: Fixed kwarg alignmene between cli <-> apiclient. (d4f0493) [JustAddRobots]
- ISSUE-020: Removed unnecessary SEL clear. (3fbce05) [JustAddRobots]
- ISSUE-020: Added apiclient and class support. (b86a98d) [JustAddRobots]

0.1.7 (2020-11-21)
------------------
- ISSUE-013: Removed unnecessary multibranch & dummy file. (b0b2e18) [JustAddRobots]

0.1.6 (2020-11-21)
------------------
- Stage: Adding dummy file for more multibranch pipeline tests. (a8bf3c7) [JustAddRobots]
- Stage: Removed dummy file for multibranch pipeline testing. (1252e5e) [JustAddRobots]
- Stage: Added dummy file to test multibranch pipeline. (4db3306) [JustAddRobots]
- Stage: Removed unnecessary $PATH check. (f7a121f) [JustAddRobots]
- Stage: Removed unnecessary $PATH check. (d9b55b6) [JustAddRobots]
- ISSUE-013: Added multibranch Jenkinsfile. (b7d35f9) [JustAddRobots]

0.1.5 (2020-11-21)
------------------
- Stage: Removed dummy file, will try Jenkins multibranch pipeline. (20213a8) [JustAddRobots]
- ISSUE-013: Added dummy file for testing webhook trigger. (6957843) [JustAddRobots]
- LOAD-010: Added echo of $PATH during build for troubleshooting. (434c1bf) [JustAddRobots]
- ISSUE-013: Added dummy file for testing webhook trigger. (57a305d) [JustAddRobots]
- Stage: Added misc fixes. (8650126) [JustAddRobots]
- Stage: Reverted changes, no 'make' in jenkins-docker, see ISSUE-010. (366d2a4) [JustAddRobots]
- Stage: Added more shell troubleshooting. (0a5c6af) [JustAddRobots]
- Stage: Added more make troubleshooting bits. (09c9ad7) [JustAddRobots]
- Stage: Added jenkinslinter, but the pre-commit hook is broken. (560ca8a) [JustAddRobots]
- Stage: Added shell $PATH echo, jenkinslint. (8b4a169) [JustAddRobots]
- LOAD-010: Added echo of $PATH during build for troubleshooting. (60e1d7d) [JustAddRobots]

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
