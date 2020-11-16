# Stage 1: Create build container

FROM hosaka.local:5000/centos:7.8-x86_64 as builder
WORKDIR /
COPY ./repofile/* /etc/yum.repos.d/
ENV TZ=America/Los_Angeles

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    yum -y install \
    git \
    infinipath-psm-devel \
    iproute \
    libgomp \
    libfabric \
    openblas \
    openblas-devel \
    openmpi3 \
    openssh-clients \
    pciutils \
    wget \
    && \
    yum clean all && rm -rf /var/cache/yum

# Stage 2: Create deployment container

FROM hosaka.local:5000/centos:7.8-x86_64
WORKDIR /
ENV TZ=America/Los_Angeles
ENV DEBUG=""
ENV RUNS=""
ENV MEM=""
ENV LOGID="${LOGID}"
ENV PREFIX="${PREFIX}"
ENV SERVER="${SERVER}"
ARG GIT_COMMIT="master"
ENV PATH="${PATH}:/usr/lib64/openmpi3/bin"

# Copy binaries used for RUN

COPY --from=builder \
    /usr/bin/git \
    /usr/bin/wget \
    /usr/bin/

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo "11.22.33.166 hosaka.local" >> /etc/hosts && \
    echo $TZ > /etc/timezone && \
    yum -y install \
    bzip2 \
    openssh-clients \
    python3 \
    python3-pip \
    which \
    && \
    yum clean all && rm -rf /var/cache/yum && \
    mkdir -p /root/.ssh && \
    wget -nv -r -l1 -np -nH --cut-dirs=3 --reject index* -P /root/.ssh/ http://hosaka.local/ark/git/DeployKeys/ && \
    chmod 600 /root/.ssh/* && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools && \
    python3 -m pip install --force-reinstall git+ssh://git@runxhpl.github.com/JustAddRobots/runxhpl.git@$GIT_COMMIT && \
    rm -rf ~/.cache/pip

# Copy binaries

COPY --from=builder \
    /usr/sbin/ip \
    /usr/sbin/lspci \
    /usr/sbin/

# Copy libraries needed by XHPL

COPY --from=builder \
    /usr/lib64/openmpi3/ \
    /usr/lib64/openmpi3/

COPY --from=builder \
    /usr/lib64/ld-linux-x86-64.so.2 \
    /usr/lib64/libbz2.so.1 \
    /usr/lib64/libc.so.6 \
    /usr/lib64/libcom_err.so.2 \
    /usr/lib64/libcrypto.so.10 \
    /usr/lib64/libdl.so.2 \
    /usr/lib64/libexpat.so.1 \
    /usr/lib64/libfabric.so.1 \
    /usr/lib64/libgcc_s.so.1 \
    /usr/lib64/libgfortran.so.3 \
    /usr/lib64/libgomp.so.1 \
    /usr/lib64/libgssapi_krb5.so.2 \
    /usr/lib64/libhwloc.so.5 \
    /usr/lib64/libibumad.so.3 \
    /usr/lib64/libibverbs.so.1 \
    /usr/lib64/libinfinipath.so.4 \
    /usr/lib64/libk5crypto.so.3 \
    /usr/lib64/libkeyutils.so.1 \
    /usr/lib64/libkmod.so.2 \
    /usr/lib64/libkrb5.so.3 \
    /usr/lib64/libkrb5support.so.0 \
    /usr/lib64/libltdl.so.7 \
    /usr/lib64/liblzma.so.5 \
    /usr/lib64/libm.so.6 \
    /usr/lib64/libmlx5.so.1 \
    /usr/lib64/libnl-3.so.200 \
    /usr/lib64/libnl-route-3.so.200 \
    /usr/lib64/libnss_files.so.2 \
    /usr/lib64/libnuma.so.1 \
    /usr/lib64/libopenblas.so.0 \
    /usr/lib64/libpci.so.3 \
    /usr/lib64/libosmcomp.so.4 \
    /usr/lib64/libpcre.so.1 \
    /usr/lib64/libpsm2.so.2 \
    /usr/lib64/libpsm_infinipath.so.1 \
    /usr/lib64/libpthread.so.0 \
    /usr/lib64/libquadmath.so.0 \
    /usr/lib64/librdmacm.so.1 \
    /usr/lib64/libresolv.so.2 \
    /usr/lib64/libselinux.so.1 \
    /usr/lib64/libssl.so.10 \
    /usr/lib64/libtinfo.so.5 \
    /usr/lib64/libucm.so.0 \
    /usr/lib64/libucp.so.0 \
    /usr/lib64/libucs.so.0 \
    /usr/lib64/libuct.so.0 \
    /usr/lib64/libutil.so.1 \
    /usr/lib64/libz.so.1 \
    /usr/lib64/

CMD runxhpl $DEBUG $MEM $RUNS $LOGID $PREFIX $SERVER
