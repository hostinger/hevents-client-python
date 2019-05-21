#!/usr/bin/env groovy

def cleanupBuild() {
    sh 'make clean'
}

node() {

    String DIST_DIR = "dist"
    String TEST_REPORTS = "reports"
    String PYENV_ROOT = "${env.WORKSPACE}/.pyenv"
    String PYENV_SHIMS = "${PYENV_ROOT}/shims"
    List<String> PYENV_VERSIONS = ['3.7.3', '3.6.8'] // Order matters. First is default.

    // No spaces around equal sign!
    List<String> buildEnv = [
        "DIST_DIR=${DIST_DIR}",
        "TEST_REPORTS=${TEST_REPORTS}",
        "PYENV_ROOT=${PYENV_ROOT}",
        "PATH=${PYENV_ROOT}/bin:${PYENV_SHIMS}:${env.PATH}"
    ]

    echo "Running ${currentBuild.fullProjectName} (build number: ${currentBuild.number}) on node name: ${env.NODE_NAME}"

    try {
        withEnv(buildEnv) {
            stage('Checkout from source version control') {
                checkout scm
            }

            stage('Cleanup Build') {
                cleanupBuild()
            }

            stage("Setup Python Environments (Pyenv)") {
                sh "git clone https://github.com/pyenv/pyenv.git ${env.PYENV_ROOT} || true"
                sh "pyenv init - >  ${env.WORKSPACE}/.pyenvrc || true"
                sh ". ${env.WORKSPACE}/.pyenvrc"

                def cmds = PYENV_VERSIONS.collectEntries {
                    version -> [
                        "Install Pyenv ${version}", {
                            sh "pyenv install -s ${version}"
                        }
                    ]
                }
                parallel(cmds)

                sh "pyenv local ${PYENV_VERSIONS.join(' ')}"
            }

            stage('Tests') {
                sh "pip install tox"

                def TOX_ENVIRONMENTS = sh(returnStdout: true, script: "tox -l").trim().split('\n')
                def cmds = TOX_ENVIRONMENTS.collectEntries({ tox_env ->
                    ["Tox Env ${tox_env}", {
                    sh "tox --parallel 1 -vve $tox_env"
                    }]
                })
                parallel(cmds)
            }


            stage("Coverage") {
                sh 'pip install coverage'
                sh "make coverage"
            }

            stage("Docs") {
                sh 'which pyenv'
                sh 'which pip'
                sh 'python --version'
                sh 'pip install sphinx'
                sh "make docs"
            }

            if (env.BRANCH_NAME == "master") {
                stage("Build Dist") {
                    sh "make dist"
                }
            }
        }

        currentBuild.result = 'SUCCESS'
    }
    catch (Exception err) {
        error = err.toString()
        echo "Build failed: ${error}"
        currentBuild.result = 'FAILURE'
    }

    // junit "${TEST_REPORTS}/*.xml'

    catchError {
        withEnv(buildEnv) {
            // There will be nothing if branch is not "master"
            if (env.BRANCH_NAME == "master") {
                archiveArtifacts artifacts: "${env.DIST_DIR}/**", fingerprint: true
            }
        }
    }

    echo "Build status: ${currentBuild.result}"
}
