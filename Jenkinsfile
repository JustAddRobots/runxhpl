#!/usr/bin/env groovy

// This Jenkinsfile automatically buids the repos tagged commits
// (releases/candidates/etc.)

def HASHLONG
def HASHSHORT
def TAG
def TAG_HASH
def BRANCH
def SERVER

def DOCKERHOST
def KUBECONFIG

// Requires "Pipeline Utility Steps" plugin
def loadProperties() {
    //props = readProperties file: "${workspace}/engcommon/builder.ini"
    def resp = httpRequest "http://hosaka.local/ini/builder.json"
    def content = resp.getContent()
    echo "${content}"
    def props = readJSON text: "${content}"
    DOCKERHOST = props["dockerhost"]
    KUBECONFIG = props["kubeconfig"]
    echo "DOCKERHOST: ${DOCKERHOST}"
    //DOCKERHOST = "hosaka.local:5000"
    //KUBECONFIG = '/opt/kube/config'
}

pipeline {
    agent any
    environment {
        ARCH = sh(returnStdout: true, script: 'uname -m').trim()
    }
    stages {
        stage ('Read INI') {
            steps {
                loadProperties()
            }
        }
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
                    SERVER = "hosaka.local:5000"
                }
                echo "BRANCH: ${BRANCH}"
                echo "DOCKERHOST: ${DOCKERHOST}"
                slackSend(
                    message: """\
                        STARTED ${env.JOB_NAME} #${env.BUILD_NUMBER},
                        v${TAG_HASH} (<${env.BUILD_URL}|Open>)
                    """.stripIndent()
                )
                sh("""\
                    make -C docker/${ARCH}/el-7 DOCKERHOST=${DOCKERHOST} \
                    ENGCOMMON_BRANCH=main build push
                """)
            }
        }
        stage ('Deploy to Kubernetes Cluster') {
            steps {
                script {
                    IMG = ("""\
                        ${DOCKERHOST}/runxhpl:\
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
                    v${TAG_HASH}, Took: ${currentBuild.durationString.replace(
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
                    v${TAG_HASH}, Took: ${currentBuild.durationString.replace(
                        ' and counting', ''
                    )} (<${env.BUILD_URL}|Open>)
                """.stripIndent()
            )
        }
    }
}
