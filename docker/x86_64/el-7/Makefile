# This Makefile automatically builds an XHPL docker container (runxhpl)
# and pushes the resulting image to the specified server.
# To run from the package top-level:
#
# $ sudo make -C docker/x86_64/el-7 DOCKERHOST=[server:port] build push
#
# EX:
# $ sudo make -C docker/x86_64/el-7 DOCKERHOST=buildbot.local:5000 build push
#
# The above one-liner can be included in a Jenkins freestyle or pipeline project.

ARCH        		:= $$(uname -m)
NAME        		:= $(DOCKERHOST)/runxhpl
HASHLONG    		:= $$(git log -1 --pretty=%H --no-merges)
HASHSHORT   		:= $$(git log -1 --pretty=%h --no-merges)
TAG         		:= $$(git describe --tags --abbrev=0)
IMGLONG     		:= ${NAME}:${TAG}-${HASHSHORT}-${ARCH}
IMGSHORT    		:= ${NAME}:${TAG}-${ARCH}
DEFAULT	    		:= ${NAME}:default-${ARCH}
ENGCOMMON_BRANCH	:= $(ENGCOMMON_BRANCH)

.PHONY: all
all: build push

build:
	@docker build --no-cache -t ${IMGLONG} --build-arg GIT_COMMIT=${HASHSHORT} --build-arg ENGCOMMON_BRANCH=${ENGCOMMON_BRANCH} --build-arg DOCKERHOST=${DOCKERHOST} .
	@docker tag ${IMGLONG} ${IMGSHORT}

push:
	@docker push ${IMGLONG}
	@docker push ${IMGSHORT}

default:
	@docker tag ${IMGLONG} ${DEFAULT}
	@docker push ${DEFAULT}
