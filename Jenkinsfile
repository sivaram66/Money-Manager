pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'sivaram66/money-manager'
        DOCKER_HUB_CREDENTIALS = 'dockerhub-sivaram66'  // Replace with your Docker Hub credentials in Jenkins
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/sivaram66/Money-Manager'  // Replace with your GitHub repo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE_NAME .'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub using Jenkins credentials
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Push the image to Docker Hub
                    sh 'docker push $DOCKER_IMAGE_NAME'
                }
            }
        }
    }
}
