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
python3 -m venv venv 
source /venv/bin/actative
pip3 install -r requirements.txt

python3 build.py lan'''
      }
    }

  }
}