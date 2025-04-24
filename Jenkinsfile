pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'sivaram66/money-manager'
        DOCKER_IMAGE_TAG = 'latest'
        DOCKER_IMAGE = "${DOCKER_HUB_REPO}:${DOCKER_IMAGE_TAG}"
        DOCKER_CREDENTIALS_ID = 'Docker-credentials'
        GIT_REPO = 'https://github.com/sivaram66/Money-Manager.git'
        GITHUB_CREDENTIALS_ID = 'github-credentials'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: "${GITHUB_CREDENTIALS_ID}",
                    url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker push ${DOCKER_IMAGE}
                        '''
                    }
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                // script {
                //     sh '''
                //     echo "Stopping and removing old container (if exists)..."
                //     docker rm -f money-manager || true

                //     echo "Running new container..."
                //     docker run -d --name money-manager -p 8000:8000 ${DOCKER_IMAGE}
                //     '''
                // }
                script {
                        withCredentials([file(credentialsId: 'budgetbuddy-backend-env', variable: 'SECRET_ENV')]) {
                                sh '''
                                cp "$SECRET_ENV" .env
                                '''
                        }
                }

                sh "docker compose down --rmi all --volumes"
                sh "docker compose up -d"

            }
        }

        stage('Cleanup (Optional)') {
            steps {
                script {
                    sh 'docker system prune -f'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}
