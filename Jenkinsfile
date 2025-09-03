pipeline {
    agent {
        docker {
            image 'docker/compose:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Build with Docker Compose') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running test...'
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u <your_dockerhub_user> --password-stdin"
                }
                sh 'docker-compose push'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down && docker-compose up -d'
            }
        }
    }
}