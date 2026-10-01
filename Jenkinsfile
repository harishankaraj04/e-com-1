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
                    echo "===== e-com-1 ====="
                    pwd
                    git remote -v
                    git branch --show-current
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
                sh '''
                    ./jenkins-venv/bin/python -m py_compile app.py
                    ./jenkins-venv/bin/python -m unittest test_app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build --no-cache -t e-commerce-app:latest .
                    docker images e-commerce-app
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    docker stop e-commerce-app || true
                    docker rm e-commerce-app || true
                    docker run -d --name e-commerce-app -p 5000:5000 --restart unless-stopped e-commerce-app:latest
                    docker ps
                '''
            }
        }

        stage('Application Test') {
            steps {
                sh '''
                    sleep 5
                    curl -f http://localhost:5000
                '''
            }
        }
    }

    post {
        success {
            echo 'e-com-1 CI/CD SUCCESS'
        }

        failure {
            echo 'e-com-1 CI/CD FAILED'
        }
    }
}
