#!/usr/bin/env groovy

/*
    This Jenkinsfile uses the Jenkins shared library. (ssh://git@git.vito.local:7999/biggeo/jenkinslib.git)
    Information about the pythonPipeline method can be found in pythonPipeline.groovy
*/

@Library('lib')_

pythonPipeline {
  package_name = 'pywig'
  wipeout_workspace = true
  wheel_repo = 'python-packages-public'
  python_version = ['3.6']
  run_tests = true
}
