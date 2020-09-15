#!/bin/env groovy
// This is a Jenkins pipeline file. It will be picked up by Jenkins and contains
// instructions this project should be built and tested.
// File contents can be validated by doing:
//    curl --user username:password -X POST -F "jenkinsfile=<Jenkinsfile" http://ci.topic.nl:8080/pipeline-model-converter/validate

// The argument to 'node' is the label Jenkins will use to allocate a build slave.
// Replace it with the name of your project. Add this label to the slave(s) that
// should build this project.
node('linux') {
    stage('Build') {
        echo('Checking out code...')
        // This command checks out the correct branch and revision
        checkout scm
        echo('Building...')
        sh('python setup.py build')
    }

    stage('Test') {
        echo('Testing...')
        sh('echo Add a command that runs automated tests here')
    }
}
