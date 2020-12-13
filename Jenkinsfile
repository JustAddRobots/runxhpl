#!/usr/bin/env groovy

// This Jenkinsfile automatically buids the repos tagged commits
// (releases/candidates/etc.)

def HASHLONG
def HASHSHORT
def TAG
def TAG_HASH
def MMP
def BRANCH
def SERVER

def DOCKERHOST
def KUBECONFIG

// Requires "Pipeline Utility Steps" plugin
def loadProperties() {
    def resp = httpRequest "http://hosaka.local/ini/builder.json"
    def content = resp.getContent()
    echo "${content}"
    def props = readJSON text: "${content}"
    echo "${props}"
    env.DOCKERHOST = props["dockerhost"]
    env.KUBECONFIG = props["kubeconfig"]
    echo "DOCKERHOST: ${DOCKERHOST}"
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
                    env.HASHLONG = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=%H --no-merges"
                    ).trim()
                    env.HASHSHORT = sh(
                        returnStdout: true,
                        script: "git log -1 --pretty=%h --no-merges"
                    ).trim()
                    env.TAG = sh(
                        returnStdout: true,
                        script: "git describe --tags --abbrev=0"
                    ).trim()
                    env.TAG_HASH = "${env.TAG}-${env.HASHSHORT}-${env.ARCH}"
                }
                echo "ARCH: ${env.ARCH}"
                echo "COMMIT: ${env.GIT_COMMIT}"
                echo "HASHLONG: ${env.HASHLONG}"
                echo "HASHSHORT: ${env.HASHSHORT}"
                echo "TAG: ${env.TAG}"
                echo "TAG_HASH: ${env.TAG_HASH}"
            }
        }
        stage ('Build Docker Container') {
            steps {
                script {
                    env.BRANCH = sh(
                        returnStdout: true,
                        script: """\
                            git show-ref | grep `git rev-parse HEAD` | 
                            awk '{ print \$2 }' | awk -F/ '{ print \$NF}'
                        """).trim()
                }
                echo "BRANCH: ${env.BRANCH}"
                echo "DOCKERHOST: ${env.DOCKERHOST}"
                slackSend(
                    message: """\
                        STARTED ${env.JOB_NAME} #${env.BUILD_NUMBER},
                        v${env.TAG_HASH} (<${env.BUILD_URL}|Open>)
                    """.stripIndent()
                )
                sh("""\
                    make -C docker/${env.ARCH}/el-7 DOCKERHOST=${env.DOCKERHOST} \
                    ENGCOMMON_BRANCH=main build push
                """)
            }
        }
        stage ('Deploy to Kubernetes Cluster') {
            steps {
                script {
                    IMG = ("""\
                        ${env.DOCKERHOST}/runxhpl:\
                        ${env.TAG_HASH}
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
        stage('Push Default Tag') {
            when {
                branch 'main'
            }
            steps {
                sh("""\
                    make -C docker/${env.ARCH}/el-7 DOCKERHOST=${env.DOCKERHOST} \
                    default
                """)
            }
        }
        stage('Delete RC Tags') {
            when {
                branch 'main'
            }
            steps {
                script {
                    (mmp, _) = "${env.TAG}".tokenize("-") // Major Minor Patch
                    env.MMP = "${mmp}"
                    echo "TAG: ${env.TAG}"
                    echo "MMP: ${env.MMP}"
                    withCredentials(usernamePassword(
                        credentialsId: 'github-runxhpl-multibranch-stage',
                        passwordVariable: 'GIT_PASSWORD',
                        usernameVariable: 'GIT_USERNAME'
                    ){
                        sh("""git push --delete origin \$(git tag -l "${env.MMP}-rc*")""")
                        sh("""git tag -d \$(git tag -l "${env.MMP}-rc*")""")
                    }
                    /*
                        sh(
                            returnStdout: false,
                            script: """\
                                git config --global credential.username {GIT_USERNAME} && \
                                git config --global credential.helper "!echo password={GITPASSWORD}; echo" && \
                                git push --delete origin \$(git tag -l "${env.MMP}-rc*") && \
                                git tag -d \$(git tag -l "${env.MMP}-rc*")
                            """
                        )
                    }
                    *//*
                    sh(
                        returnStdout: false,
                        script: """\
                            git push --delete origin \$(git tag -l "${env.MMP}-rc*")
                        """
                    )
                    sh(
                        returnStdout: false,
                        script: """\
                            git tag -d \$(git tag -l "${env.MMP}-rc*")
                        """
                    )
                    */
                //sh("""git push --delete origin \$(git tag -l "${env.MMP}-rc*")""")
                //sh("""git tag -d \$(git tag -l "${env.MMP}-rc*")""")
                }
            }
        }
    }
    post {
        success {
            slackSend(
                color: "good",
                message: """\
                    SUCCESS ${env.JOB_NAME} #${env.BUILD_NUMBER},
                    v${env.TAG_HASH}, Took: ${currentBuild.durationString.replace(
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
