pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'sivaram66/money-manager'
        DOCKER_IMAGE_TAG = "${DOCKER_IMAGE_NAME}:latest"  // Optionally add a tag
        DOCKER_HUB_CREDENTIALS = 'dockerhub-sivaram66'  // Name of the credentials ID
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/sivaram66/Money-Manager'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker --version'  // Optional: Verify Docker installation
                    sh 'docker build -t $DOCKER_IMAGE_TAG .'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Use Jenkins credentials to login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-sivaram66', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    }
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sh 'docker push $DOCKER_IMAGE_TAG'
                }
            }
        }
    }
}
