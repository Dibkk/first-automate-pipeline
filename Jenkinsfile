pipeline {
    agent {
        docker {
            image 'docker:24.0.2'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        REGISTRY = "docker.io/kerdsuk"
        IMAGE_NAME = "python-project"
        TAG = "${env.GIT_COMMIT?.take(7) ?: env.BUILD_NUMBER}"
        FULL_IMAGE = "${REGISTRY}/${IMAGE_NAME}:${TAG}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh "docker build --pull -t ${FULL_IMAGE} ."
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin ${REGISTRY}"
                    sh "docker push ${FULL_IMAGE}"
                    sh "docker logout ${REGISTRY}"
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                sh '''
                kubectl apply -f server-deployment.yml
                kubectl apply -f mongo-deployment.yml
                '''
            }
        }
    }

    post {
        always {
            sh "docker image rm ${FULL_IMAGE} || true"
        }
    }
}