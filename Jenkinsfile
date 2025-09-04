pipeline {
    agent {
        docker {
            image 'docker:24.0.2'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        REGISTRY = "kerdsuk"
        IMAGE_NAME = "kerdsuk/python-project"
        TAG = "${env.GIT_COMMIT?.take(7) ?: env.BUILD_NUMBER}"
        FULL_IMAGE = "${env.REGISTRY}/${env.IMAGE_NAME}:${env.TAG}"
    }

    stages {

        stage('Build') {
            steps {
                sh "docker build -t ${FULL_IMAGE} ."
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
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    // write kubeconfig to KUBECONFIG path for kubectl
                    sh 'export KUBECONFIG=$KUBECONFIG_FILE && kubectl config view --minify'
                    // update deployment image and wait for rollout
                    sh "export KUBECONFIG=$KUBECONFIG_FILE && kubectl set image deployment/server-deployment server=${FULL_IMAGE} --record"
                    sh "export KUBECONFIG=$KUBECONFIG_FILE && kubectl rollout status deployment/server-deployment --timeout=120s"
                }
            }
        }
    }

    post {
        always {
            sh "docker image rm ${FULL_IMAGE} || true"
        }
    }
}