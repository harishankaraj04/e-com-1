pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Application Check') {
            steps {
                sh '''
                    echo "Checking e-com-1"
                    ls -la
                    python3 --version
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    rm -rf jenkins-venv
                    python3 -m venv jenkins-venv
                    ./jenkins-venv/bin/python --version
                    ./jenkins-venv/bin/pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    ./jenkins-venv/bin/pip install --upgrade pip
                    ./jenkins-venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                ./jenkins-venv/bin/python -m py_compile app.py
                ./jenkins-venv/bin/python -m unittest test_app.py
            }
        }
    }

    post {
        success {
            echo 'e-com-1 CI SUCCESS'
        }

        failure {
            echo 'e-com-1 CI FAILED'
        }
    }
}
