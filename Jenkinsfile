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
                sh '''
                    ./jenkins-venv/bin/python -m py_compile app.py
                    ./jenkins-venv/bin/python -m unittest test_app.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t e-commerce-app:latest .
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    echo "Stopping old container..."
                    docker stop e-commerce-app || true

                    echo "Removing old container..."
                    docker rm e-commerce-app || true

                    echo "Starting new container..."
                    docker run -d \
                        --name e-commerce-app \
                        -p 5000:5000 \
                        --restart unless-stopped \
                        e-commerce-app:latest

                    echo "Container status:"
                    docker ps
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
