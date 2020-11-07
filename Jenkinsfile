#!/usr/bin/env groovy

def HASHLONG
def HASHSHORT
def TAG
def TAG_HASH
def BRANCH
def SERVER

pipeline {
    agent any
    environment {
        ARCH = sh(returnStdout: true, script: 'uname -m').trim()
    }
    stages {
        stage ('Create Tag Hash') {
            steps {
                script {
                    HASHLONG = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=%H --no-merges"
                    ).trim()
                    HASHSHORT = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=%h --no-merges"
                    ).trim()
                    TAG = sh(
                        returnStdout: true,
                        script: "git describe --tags --abbrev=0"
                    ).trim()
                    TAG_HASH = "${TAG}-${HASHSHORT}-${ARCH}"
                }
                echo "ARCH: ${env.ARCH}"
                echo "COMMIT: ${env.GIT_COMMIT}"
                echo "HASHLONG: ${HASHLONG}"
                echo "HASHSHORT: ${HASHSHORT}"
                echo "TAG: ${TAG}"
                echo "TAG_HASH: ${TAG_HASH}"
            }
        }
        stage ('Build Docker Container') {
            steps {
                script {
                    BRANCH = sh(
                        returnStdout: true,
                        script: """\
                            git show-ref | grep `git rev-parse HEAD` | 
                            awk '{ print \$2 }' | awk -F/ '{ print \$NF}'
                        """).trim()
                    SERVER = "${BRANCH == 'master' ? 'iso' : 'bmstagedev'}"
                }
                echo "BRANCH: ${BRANCH}"
                echo "SERVER: ${SERVER}"
                slackSend(
                    message: """\
                        STARTED ${env.JOB_NAME} #${env.BUILD_NUMBER},
                        v${TAG_HASH} (<${env.BUILD_URL}|Open>)
                    """.stripIndent()
                )
                sh("""\
                    make -C docker/${ARCH}/el-7 SERVER=${SERVER} build push
                """)
            }
        }
        stage ('Deploy to Kubernetes Cluster') {
            steps {
                script {
                    IMG = ("""\
                        ${SERVER}.penguincomputing.com:5000/runxhpl:\
                        ${TAG_HASH}
                    """.stripIndent().replaceAll("\\s","")
                    )
                }
                sh("""\
                        python3 /usr/local/bin/runkubejobs \
                        -d -t runxhpl \
                        -p /var/lib/jenkins/workspace/logs \
                        -n all -i ${IMG}
                    """.stripIndent()
                )
            }
        }
    }
    post {
        success {
            slackSend(
                color: "good",
                message: """\
                    SUCCESS ${env.JOB_NAME} #${env.BUILD_NUMBER},
                    v${TAG_HASH},
                    Took: ${currentBuild.durationString.replace(
                        ' and counting', ''
                    )} (<${env.BUILD_URL}|Open>)
                """.stripIndent()
            )
        }
        failure {
            slackSend(
                color: "danger",
                message: """\
                    FAILURE ${env.JOB_NAME} #${env.BUILD_NUMBER},
                    v${TAG_HASH}, 
                    Took: ${currentBuild.durationString.replace(
                        ' and counting', ''
                    )} (<${env.BUILD_URL}|Open>)
                """.stripIndent()
            )
        }
    }
}
