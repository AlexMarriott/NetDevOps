pipeline {
  agent {
    node {
      label 'BuildServer'
    }

  }
  stages {
    stage('Run Tests') {
      agent {
        node {
          label 'BuildServer'
        }

      }
      steps {
        sh '''#!/bin/bash
pip3 install -r requirements.txt

python3 build.py lan'''
      }
    }

  }
}