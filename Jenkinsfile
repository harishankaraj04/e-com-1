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

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m py_compile app.py
                    echo "Test successful"
                '''
            }
        }
    }

    post {
        success {
            echo "e-com-1 CI SUCCESS"
        }
        failure {
            echo "e-com-1 CI FAILED"
        }
    }
}
